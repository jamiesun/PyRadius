#!/usr/bin/env python
#coding:utf-8
from settings import radiuslog
from settings import ticketlog
from logging import DEBUG
import datetime
import service
import json

STATUS_TYPE_START   = 1
STATUS_TYPE_STOP    = 2
STATUS_TYPE_UPDATE  = 3
STATUS_TYPE_NAS_ON  = 7
STATUS_TYPE_NAS_OFF = 8


class _AccountingRequestHandler():    
    def process(self,req):
        if radiuslog.isEnabledFor(DEBUG):
            radiuslog.debug("Received an accounting request")
            radiuslog.debug( "Attributes: ")
            for attr in req.keys():
                radiuslog.debug( "%s: %s" % (attr, req[attr]))

        reply = req.CreateReply()
        reply.source = req.source
        req.sock.sendto(reply.ReplyPacket(), reply.source)

        nasaddr = req.get_nasaddr()
        nas = service.get_nas(nasaddr)         
        
        acct_status_type  = req.get_acctstatustype()

        if acct_status_type == STATUS_TYPE_START:
            return self.start_accounting(req,nas)
        elif acct_status_type == STATUS_TYPE_STOP:
            return self.stop_accounting(req,nas)
        elif acct_status_type == STATUS_TYPE_UPDATE:
            return self.update_accounting(req,nas)
        elif acct_status_type == STATUS_TYPE_NAS_ON or \
             acct_status_type == STATUS_TYPE_NAS_OFF  :
            return self.nasonoff_accounting(nasaddr,acct_status_type)     
        else:
            return                                        

    def start_accounting(self,req,nas):
        service.incr_stat(service.STAT_ACCT_START)
        _key = '%s_%s'%(nas.ip_addr,req.get_acctsessionid())
        if service.is_online(_key):
            radiuslog.error('[Acct] accounting of start is repeated')
            return

        user = service.get_user(req.get_username())

        if not user:
            radiuslog.error("[Acct] Received an accounting request but user[%s] not exists"%req.get_username())
            return

        online = dict(user = user,
            nas = nas,
            sessionid = req.get_acctsessionid(),
            acctstarttime = datetime.datetime.now().strftime( "%Y-%m-%d %H:%M:%S"),
            framedipaddr = req.get_framedipaddr(),
            macaddr = req.get_macaddr(),
            nasportid = req.get_nasportid(),
            startsource = STATUS_TYPE_START)

        service.add_online(_key,online)

        if radiuslog.isEnabledFor(DEBUG):
            radiuslog.info('[Acct] User[%s],Nas[%s] billing starting'%(user.user_name,nas.ip_addr))


    def stop_accounting(self,req,nas):
        _key = '%s_%s'%(nas.ip_addr,req.get_acctsessionid())
        service.incr_stat(service.STAT_ACCT_STOP)
        online = service.rmv_online(_key)

        ticket = req.get_ticket()

        if online is None:
            sessiontime = req.get_acctsessiontime()
            _stoptime = datetime.datetime.now()
            _starttime = _stoptime + datetime.timedelta(seconds=-sessiontime)
            ticket['acctstarttime'] = _starttime.strftime( "%Y-%m-%d %H:%M:%S")
            ticket['acctstoptime'] = _stoptime.strftime( "%Y-%m-%d %H:%M:%S")
            ticket['startsource'] = STATUS_TYPE_STOP
            ticket['stopsource'] = STATUS_TYPE_STOP
            ticket['nodeid'] = nas.id
        else:
            ticket['nodeid'] = online['user'].node_id
            ticket['acctstarttime'] = online['acctstarttime']
            ticket['acctstoptime'] = datetime.datetime.now().strftime( "%Y-%m-%d %H:%M:%S")
            ticket['startsource'] = online['startsource']
            ticket['stopsource'] = STATUS_TYPE_STOP
            ticket['framedipaddr'] = online['framedipaddr']

        if radiuslog.isEnabledFor(DEBUG):
            radiuslog.info('[Acct] User[%s],Nas[%s] billing stop'%(req.get_username(),nas.ip_addr))

        user = service.get_user(req.get_username())
        if not user:
            ticketlog.info(json.dumps(ticket))
            return

        product  = service.get_product(user.product_id)

        if product.policy == 0:
            sessiontime = round(req.get_acctsessiontime()/60,0)
            usedfee = round(sessiontime/60*product.fee_price,0)
            remaind = round(sessiontime%60,0)
            if remaind > 0 :
                usedfee = usedfee + round(remaind*product.fee_price/60,0);
            balance = user.balance - usedfee

            balance = balance < 0 and 0 or balance
            service.update_user_balance(user.user_name,balance)

            ticket['actualfee'] = usedfee
            ticket['acctfee'] = usedfee
            ticket['isdeduct'] = 1
            ticketlog.info("ticket:%s"%json.dumps(ticket))
        else :
            ticket['actualfee'] = 0
            ticket['acctfee'] = 0
            ticket['isdeduct'] = 0
            ticketlog.info("ticket:%s"%json.dumps(ticket))

    def update_accounting(self,req,nas):
        service.incr_stat(service.STAT_ACCT_UPDATE)
        _key = '%s_%s'%(nas.ip_addr,req.get_acctsessionid())

        online = service.get_online(_key)
        if online is None:
            user = service.get_user(req.get_username())
            if not user:
                radiuslog.error("[Acct] Received an accounting request but user[%s] not exists"%req.get_username())
                return            
            sessiontime = req.get_acctsessiontime()
            updatetime = datetime.datetime.now()

            _starttime = updatetime + datetime.timedelta(seconds=-sessiontime)       

            online = dict(user = user,
                nas = nas,
                sessionid = req.get_acctsessionid(),
                acctstarttime = _starttime,
                framedipaddr = req.get_framedipaddr(),
                macaddr = req.get_macaddr(),
                nasportid = req.get_nasportid(),
                startsource = STATUS_TYPE_UPDATE)

            service.add_online(_key,online)       
        else:
            online['framedipaddr'] = req.get_framedipaddr()

    def nasonoff_accounting(self,nasaddr,status_type):
    
        for key in service.get_online_keys():
            if key.startswith(nasaddr):
                online = service.rmv_online(key)
                stoptime = datetime.datetime.now()
                ticket = dict(
                    nodeid = online['user'].node_id,
                    nasaddr = nasaddr,
                    username = online['user'].user_name,
                    sessionid = online['sessionid'],
                    acctstarttime = online['acctstarttime'],
                    acctstoptime = stoptime.strftime( "%Y-%m-%d %H:%M:%S"),
                    acctsessiontime = (stoptime - datetime.datetime.strptime\
                        (online['acctstarttime'],"%Y-%m-%d %H:%M:%S").seconds),
                    framedipaddr = online['framedipaddr'],
                    macaddr = online['macaddr'],
                    nasportid = online['nasportid'],
                    stopsource = status_type
                )
                ticketlog.info("ticket:%s"%json.dumps(ticket))

        if status_type == STATUS_TYPE_NAS_ON :
            service.incr_stat(service.STAT_ACCT_ON)
            radiuslog.info("[Acct] nas [%s] on : success"%nasaddr)
        elif status_type == STATUS_TYPE_NAS_OFF:
            service.incr_stat(service.STAT_ACCT_OFF)
            radiuslog.info("[Acct] nas [%s] off : success"%nasaddr)



_handler = _AccountingRequestHandler()

def accountingHandler(req):
    _handler.process(req)