#!/usr/bin/env python
#coding:utf-8
from pyrad import packet
from settings import acctlog as log
from logging import DEBUG
import datetime
import service
import utils

STATUS_TYPE_START   = 1
STATUS_TYPE_STOP    = 2
STATUS_TYPE_UPDATE  = 3
STATUS_TYPE_NAS_ON  = 7
STATUS_TYPE_NAS_OFF = 8


class _AccountingRequestHandler():    
    def process(self,req):
        if log.isEnabledFor(DEBUG):
            log.debug("Received an accounting request")
            log.debug( "Attributes: ")
            for attr in req.keys():
                log.debug( "%s: %s" % (attr, req[attr]))

        reply = req.CreateReply()
        reply.source = req.source
        req.sock.sendto(reply.ReplyPacket(), reply.source)

        nasaddr = req.get_nasaddr()
        nas = service.get_nas(nasaddr)         
        
        acct_status_type  = req.get_acctstatustype()

        if acct_status_type == STATUS_TYPE_START:
            return self.start_accounting(req,nas)
        elif acct_status_type == STATUS_TYPE_START:
            return self.stop_accounting(req,nas)
        elif acct_status_type == STATUS_TYPE_START:
            return self.update_accounting(req,nas)
        elif acct_status_type == STATUS_TYPE_START:
            return self.nason_accounting(req,nas)
        elif acct_status_type == STATUS_TYPE_START:
            return self.nasoff_accounting(req,nas)        
        else:
            return                                        

    def start_accounting(self,req,nas):
        _key = '%s_%s'%(nas.ip_addr,req.get_acctsessionid())
        if service.is_online(_key):
            log.error('accounting of start is repeated')
            return

        service.incr_stat(service.STAT_ACCT_START)

        user = service.get_user(req.get_username())

        if not user:
            log.error("user not exists")

        online = dict(user = user,
            nas = nas,
            sessionid = req.get_acctsessionid(),
            acctstarttime = datetime.datetime.now().strftime( "%Y-%m-%d %H:%M:%S"),
            framedipaddr = req.get_framedipaddr(),
            macaddr = req.get_macaddr(),
            nasportid = req.get_nasportid(),
            startsource = STATUS_TYPE_START)

        service.add_online(_key,online)

        log.info('User[%s],Nas[%s] billing begins'%(user.user_name,nas.ip_addr))


    def stop_accounting(self,req,nas):
        _key = '%s_%s'%(nas.ip_addr,req.get_acctsessionid())
        service.incr_stat(service.STATUS_TYPE_STOP)
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
            pass




    def update_accounting(self):
        pass
    def nason_accounting(self):
        pass
    def nasoff_accounting(self):
        pass

                                   

_handler = _AccountingRequestHandler()

def accountingHandler(req):
    _handler.process(req)