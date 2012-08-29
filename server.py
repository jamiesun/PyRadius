#!/usr/bin/env python
#coding:utf-8

import socket, asyncoro
from pyrad import dictionary
from pyrad import host
from pyrad import packet
from settings import log 
from handler import AccessRequestHandler
from handler import AccountingRequestHandler
import sys

MaxPacketSize = 8192

class PacketError(Exception):
    """Exception class for bogus packets

    PacketError exceptions are only used inside the Server class to
    abort processing of a packet.
    """

handlers = {
    packet.AccessRequest : AccessRequestHandler(),
    packet.AccountingRequest : AccountingRequestHandler()
}

class RudiusServer(host.Host):

    def __init__(self, address=[],hosts={},
                       authport=1812, acctport=1813,
                       secret="secret",dict=dictionary.Dictionary()):
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



    def data_received(self,sock,coro=None):
        while True:
            try:
                data, (host, port) = yield sock.recvfrom(MaxPacketSize)
                if host not in self.hosts:
                    log.error(u'非法的请求 ' + host)
                    continue
            except:
                continue

            try:
                pkt = self.CreatePacket(packet=data)
            except packet.PacketError as err:
                log.error(u'数据包错误: ' + str(err))
                return            

            pkt.source = (host, port)
            pkt.secret = self.secret
            pkt.sock = sock

            try:
                pkt_handler = handlers[pkt.code]
                yield pkt_handler.process(pkt)
            except PacketError as err:
                log.error(u'请求处理失败 %s: %s' % (host, str(err)))  



if __name__ == '__main__':
    hosts = ['198.168.8.139','127.0.0.1']
    try:
        RudiusServer(address=['198.168.8.139','127.0.0.1'],hosts=hosts)
    except KeyboardInterrupt:
        sys.exit()
