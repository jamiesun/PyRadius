#!/usr/bin/env python
#coding:utf-8
from gevent.server import DatagramServer
from pyrad import dictionary
from pyrad import host
from settings import log 
from access_handler import accessHandler
from accounting_handler import accountingHandler
import sys
import six
import utils
import gevent


MaxPacketSize = 8192


class PacketError(Exception):
    """Exception class for bogus packets
    """

class RudiusAuthServer(DatagramServer):

    def __init__(self, address,hosts={},secret=six.b("secret"),
                       dict=dictionary.Dictionary("dictionary"),pool_szie=10):
        DatagramServer.__init__('%:%'%address)
        self.hosts = hosts
        self.address = address
        self.dict = dict
        self.secret = secret

    def handle(self,data, address):
        if address[0] not in self.hosts:
            log.error(u'Illegal request' + host)
            return 

        try:
            pkt = utils.AuthPacket2(packet=data,dict=self.dict,secret=self.secret)
            pkt.source,pkt.sock = address,self.socket
            accessHandler(pkt)     
        except Exception as err:
            log.error(u'process packet error:' + str(err))  

class RudiusAcctServer(DatagramServer):

    def __init__(self, address,hosts={},secret=six.b("secret"),
                       dict=dictionary.Dictionary("dictionary"),pool_szie=10):
        DatagramServer.__init__('%:%'%address)
        self.hosts = hosts
        self.address = address
        self.dict = dict
        self.secret = secret

    def handle(self,data, address):
        if address[0] not in self.hosts:
            log.error(u'Illegal request' + host)
            return 

        try:
            pkt = self.utils.AcctPacket2(packet=data,dict=self.dict,secret=self.secret)
            pkt.source,pkt.sock = address,self.socket
            accountingHandler(pkt)    
        except Exception as err:
            log.error(u'process packet error:' + str(err))     


if __name__ == '__main__':
    hosts = ['198.168.8.139','127.0.0.1']

    authsrv = RudiusAuthServer(address=('0.0.0.0',1812),hosts=hosts)
    acctsrv = RudiusAuthServer(address=('0.0.0.0',1813),hosts=hosts)

    job1 = gevent.spawn(authsrv.serve_forever)
    job2 = gevent.spawn(acctsrv.serve_forever)
    gevent.joinall([job1, job2])
    # gevent.run()



# while True:
#     try:
#         x = sys.stdin.readline()
#     except KeyboardInterrupt:
#         break