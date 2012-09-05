#!/usr/bin/env python
#coding:utf-8
import socket, asyncoro
from pyrad import dictionary
from pyrad import host
from pyrad import packet
from settings import log 
from access_handler import AccessRequestHandler
from accounting_handler import AccountingRequestHandler
import sys
import six
import utils

MaxPacketSize = 8192

class PacketError(Exception):
    """Exception class for bogus packets
    """

handlers = {
    packet.AccessRequest : AccessRequestHandler(),
    packet.AccountingRequest : AccountingRequestHandler()
}

class RudiusServer(host.Host):

    def __init__(self, address=[],hosts={},
                       authport=1812, acctport=1813,
                       secret=six.b("secret"),dict=dictionary.Dictionary()):
        host.Host.__init__(self,authport,acctport,dict=dict)
        self.hosts = hosts
        self.address = address
        self.authport = authport
        self.acctport = acctport        
        self.secret = secret

        if not self.address:
            self.address = ['127.0.0.1']

        for addr in self.address:
            # start auth listen
            authsock = asyncoro.AsynCoroSocket(socket.socket(socket.AF_INET, socket.SOCK_DGRAM))
            authsock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            authsock.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,1024*10*20)
            authsock.bind((addr, self.authport))
            asyncoro.Coro(self.data_received,authsock)

            # start acct listen
            acctsock = asyncoro.AsynCoroSocket(socket.socket(socket.AF_INET, socket.SOCK_DGRAM))
            acctsock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            acctsock.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,1024*10*20)
            acctsock.bind((addr, self.acctport))
            asyncoro.Coro(self.data_received,acctsock)     
           
    def CreateAuthPacket(self, **args):
        return utils.AuthPacket2(dict=self.dict,**args)

    def data_received(self,sock,coro=None):
        while True:
            try:
                data, (host, port) = yield sock.recvfrom(MaxPacketSize)
                if host not in self.hosts:
                    log.error('Illegal request' + host)
                    continue
            except:
                continue

            try:
                pkt = self.CreateAuthPacket(packet=data,secret=self.secret)
            except packet.PacketError as err:
                log.error('Packet error:' + str(err))
                return            

            pkt.source = (host, port)
            pkt.sock = sock

            try:
                pkt_handler = handlers[pkt.code]
                yield pkt_handler.process(pkt)
            except Exception as err:
                import traceback
                traceback.print_exc()
                log.error('Request process failed %s: %s' % (host, str(err)))  



if __name__ == '__main__':
    hosts = ['198.168.8.139','127.0.0.1']
    try:
        RudiusServer(address=['198.168.8.139','127.0.0.1'],hosts=hosts)
    except KeyboardInterrupt:
        sys.exit()
