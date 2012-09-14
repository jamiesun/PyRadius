#!/usr/bin/env python
#coding:utf-8
from gevent.server import DatagramServer
from gevent import socket
from access_handler import accessHandler
from accounting_handler import accountingHandler
from pyrad import dictionary,host
from settings import radiuslog 
import six
import utils
import gevent
import service

MaxPacketSize = 8192


class RudiusAuthServer(DatagramServer):

    def __init__(self, address,nases={},dict=dictionary.Dictionary("dictionary")):
        DatagramServer.__init__(self,address)
        self.nases = nases
        self.address = address
        self.dict = dict
        self.start()
        self.socket.setsockopt(socket.SOL_SOCKET,
            socket.SO_RCVBUF,10240000)

    def handle(self,data, address):
        nas = self.nases.get(address[0])
        if not nas:
            radiuslog.error(u'Illegal request from %s:%s' % address)
            return 

        try:
            pkt = utils.AuthPacket2(packet=data,dict=self.dict,secret=str(nas.auth_secret))
            pkt.source,pkt.sock = address,self.socket
            gevent.spawn(accessHandler,pkt)  
            #self.pool.apply_async(accessHandler,(pkt))   
        except Exception as err:
            radiuslog.error(u'process packet error:' + str(err))  


class RudiusAcctServer(DatagramServer):

    def __init__(self, address,nases={},dict=dictionary.Dictionary("dictionary")):
        DatagramServer.__init__(self,address)
        self.nases = nases
        self.address = address
        self.dict = dict
        self.start()
        self.socket.setsockopt(socket.SOL_SOCKET,
            socket.SO_RCVBUF,10240000)

    def handle(self,data, address):
        nas = self.nases.get(address[0])
        if not nas:
            radiuslog.error(u'Illegal request from %s:%s' % address)
            return 

        try:
            pkt = utils.AcctPacket2(packet=data,dict=self.dict,secret=str(nas.acct_secret))
            pkt.source,pkt.sock = address,self.socket
            gevent.spawn(accountingHandler,pkt)    
        except Exception as err:
            radiuslog.error(u'process packet error:' + str(err))     


if __name__ == '__main__':

    nases = dict((nas.ip_addr,nas) for nas in service.get_nas_all())
    authsrv = RudiusAuthServer(address=('0.0.0.0',1812),nases=nases)
    acctsrv = RudiusAcctServer(address=('0.0.0.0',1813),nases=nases)
    gevent.run()
    
