#!/usr/bin/env python
#coding:utf-8

from pyrad import packet
from settings import log

class Handler():
    def process(self,pkt):
        pass


class AccessRequestHandler(Handler):
    """认证包处理
    """    
    def process(self,pkt):
        log.debug("Received an authentication request")
        log.debug("Attributes: ")
        for attr in pkt.keys():
            log.debug( "%s: %s" % (attr, pkt[attr]))

        reply = pkt.CreateReply()
        reply.source = pkt.source
        reply.code=packet.AccessAccept
        pkt.sock.sendto(reply.ReplyPacket(), reply.source)

class AccountingRequestHandler(Handler):
    """记账包处理
    """        
    def process(self,pkt):
        log.debug("Received an accounting request")
        log.debug( "Attributes: ")
        for attr in pkt.keys():
            log.debug( "%s: %s" % (attr, pkt[attr]))

        reply = pkt.CreateReply()
        reply.source = pkt.source
        reply.code=packet.AccessAccept
        pkt.sock.sendto(reply.ReplyPacket(), reply.source)
