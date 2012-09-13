#!/usr/bin/env python
#coding:utf-8
from pyrad import packet
from settings import radiuslog
from logging import DEBUG
import service
import utils

class _AccessRequestHandler(): 

    def process(self,req):
        attr_keys = req.keys()
        if radiuslog.isEnabledFor(DEBUG):
            radiuslog.debug("::Received an authentication request")
            radiuslog.debug("Attributes: ")        
            for attr in attr_keys:
                radiuslog.debug( "%s: %s" % (attr, req[attr]))

        nasaddr = req.get_nasaddr()
        macaddr = req.get_macaddr()
        nas = service.get_nas(nasaddr)

        # check roster 
        if service.in_black_roster(macaddr):
            return self.send_reject(req,nas,'user in black roster')

        vlanid,vlanid2 = req.get_vlanids()
        username1 = req.get_username()
        domain = None
        username2 = username1
        if "@" in username1:
            username2 = username1[:username1.index("@")]
            req["User-Name"] = username2
            domain = username1[username1.index("@")+1:]

        if not service.user_exists(username2):
            return self.send_reject(req,nas,'user not exists')

        user = service.get_user(username2)

        if user.status != 1:
            return self.send_reject(req,nas,'Invalid user status')          

        if domain and domain not in user.domain_code:
            return self.send_reject(req,nas,'user domain does not match')       

        if nasaddr not in service.get_nas_ips(user.node_id):   
            return self.send_reject(req,nas,'node does not match')

        if not utils.is_valid_date(user.auth_begin_date,user.auth_end_date):
            return self.send_reject(req,nas,'user is not effective or expired')

        userpwd = utils.decrypt(user.password)
        if not req.is_valid_pwd(userpwd):
            return self.send_reject(req,nas,'user password does not match')

        uproduct = service.get_product(user.product_id)
        if not uproduct:
            return self.send_reject(req,nas,'user product does not match')

        if uproduct.policy == service.POLICY_TIMING and user.time_length <= 0:
            return self.send_reject(req,nas,'user does not have the time length')

        if not self.verify_macaddr(user,macaddr):
            return self.send_reject(req,nas,'user macaddr bind not match')

        valid_vlanid = self.verify_vlan(user,vlanid,vlanid2)
        if valid_vlanid == 1:
            return self.send_reject(req,nas,'user vlanid does not match')            
        elif valid_vlanid == 2:
            return self.send_reject(req,nas,'user vlanid2 does not match')    

        if user.concur_number > 0:
            if user.concur_number <= service.get_online_num(user.user_name):
                return self.send_reject(req,nas,'user concur_number control')  
        return self.send_accept(req,nas,**dict(ipaddr=user.ip_addr,
                      bandcode=uproduct.bandwidth_code,
                      input_max_limit=str(uproduct.input_max_limit),
                      output_max_limit=str(uproduct.output_max_limit),
                      input_rate_code=uproduct.input_rate_code,
                      output_rate_code=uproduct.output_rate_code,
                      domain_code=user.domain_code))

    def verify_macaddr(self,user,macaddr):
        if user.user_mac == 0:
            return True
        if not user.mac_addr:
            if macaddr:
                service.set_user_mac(user.user_name,macaddr)
                return True
        else:
            return user.macaddr.lower() != macaddr.lower()

    def verify_vlan(self,user,vlanid,vlanid2):
        if user.user_vlan == 0:
            return 0
        if user.vlan_id == 0:
            if vlanid != 0 and vlanid != 4096:
                service.set_user_vlanid(user.user_name,vlanid)
        else:
            if user.vlan_id != vlanid:
                return 1

        if user.vlan_id2 == 0:
            if vlanid2 != 0 and vlanid2 != 4096:
                service.set_user_vlanid2(user.user_name,vlanid2)
        else:
            if user.vlan_id2 != vlanid2:
                return 1


    def send_reject(self,req,nas,err):
        service.incr_stat(service.STAT_AUTH_REJECT)
        reply = req.CreateReply(msg=err)
        reply.source = req.source
        reply.code=packet.AccessReject
        # import pdb
        # pdb.set_trace()
        req.sock.sendto(reply.ReplyPacket(), reply.source)   

        radiuslog.error("[Auth]  send an authentication reject,err:%s"%err)        

    def send_accept(self,req,nas,**args):
        service.incr_stat(service.STAT_AUTH_ACCEPT)
        reply = req.CreateReply()
        reply.source = req.source
        reply.code=packet.AccessAccept

        if args:
            reply.set_framed_ip_addr(args.get("ipaddr"))
            reply.set_filter_id(nas.vendor_id,args.get("bandcode"))
            reply.set_special_str(nas.vendor_id,"context",args.get("domain_code"))
            reply.set_special_int(nas.vendor_id,"input_max_limit",args.get("input_max_limit"))
            reply.set_special_int(nas.vendor_id,"output_max_limit",args.get("output_max_limit"))
            reply.set_special_str(nas.vendor_id,"input_rate_code",args.get("input_rate_code"))
            reply.set_special_str(nas.vendor_id,"output_rate_code",args.get("output_rate_code"))

        req.sock.sendto(reply.ReplyPacket(), reply.source)     

        if radiuslog.isEnabledFor(DEBUG):
            radiuslog.debug("[Auth] send an authentication accept,user[%s],nas[%s]"\
                %(req.get_username(),nas.ip_addr))

_handler = _AccessRequestHandler()

def accessHandler(req):
    _handler.process(req)