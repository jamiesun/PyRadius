#!/usr/bin/env python
#coding:utf-8
from gevent.server import DatagramServer
from gevent import socket
from access_handler import accessHandler
from accounting_handler import accountingHandler
from pyrad import dictionary,host
from settings import radiuslog 
from logging import DEBUG
import six
import utils
import gevent

MaxPacketSize = 8192

hosts = ['198.168.8.139','127.0.0.1']

class RudiusAuthServer(DatagramServer):

    def __init__(self, address,hosts={},secret=six.b("secret"),
                       dict=dictionary.Dictionary("dictionary")):
        DatagramServer.__init__(self,address)
        self.hosts = hosts
        self.address = address
        self.dict = dict
        self.secret = secret
        self.start()
        self.socket.setsockopt(socket.SOL_SOCKET,
            socket.SO_RCVBUF,10240000)

    def handle(self,data, address):
        if address[0] not in self.hosts:
            radiuslog.error(u'Illegal request' + host)
            return 

        try:
            pkt = utils.AuthPacket2(packet=data,dict=self.dict,secret=self.secret)
            pkt.source,pkt.sock = address,self.socket
            gevent.spawn(accessHandler,pkt)  
            #self.pool.apply_async(accessHandler,(pkt))   
        except Exception as err:
            radiuslog.error(u'process packet error:' + str(err))  


class RudiusAcctServer(DatagramServer):

    def __init__(self, address,hosts={},secret=six.b("secret"),
                       dict=dictionary.Dictionary("dictionary")):
        DatagramServer.__init__(self,address)
        self.hosts = hosts
        self.address = address
        self.dict = dict
        self.secret = secret
        self.start()
        self.socket.setsockopt(socket.SOL_SOCKET,
            socket.SO_RCVBUF,10240000)

    def handle(self,data, address):
        if radiuslog.isEnabledFor(DEBUG):
            radiuslog.debug("accept :%s:%s"%address)
        if address[0] not in self.hosts:
            radiuslog.error(u'Illegal request' + host)
            return 

        try:
            pkt = utils.AcctPacket2(packet=data,dict=self.dict,secret=self.secret)
            pkt.source,pkt.sock = address,self.socket
            gevent.spawn(accountingHandler,pkt)    
        except Exception as err:
            radiuslog.error(u'process packet error:' + str(err))     


if __name__ == '__main__':
    authsrv = RudiusAuthServer(address=('0.0.0.0',1812),hosts=hosts)
    acctsrv = RudiusAcctServer(address=('0.0.0.0',1813),hosts=hosts)
    gevent.run()
    
