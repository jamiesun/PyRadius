#!/usr/bin/env python
#coding:utf-8
from __future__ import unicode_literals  
from pyrad import packet
from settings import log
from logging import DEBUG
import service
import utils



class AccountingRequestHandler():    
    def process(self,pkt):
        log.debug("Received an accounting request")
        log.debug( "Attributes: ")
        for attr in pkt.keys():
            log.debug( "%s: %s" % (attr, pkt[attr]))

        reply = pkt.CreateReply()
        reply.source = pkt.source
        reply.code=packet.AccessAccept
        pkt.sock.sendto(reply.ReplyPacket(), reply.source)
