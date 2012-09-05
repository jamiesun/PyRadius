#!/usr/bin/env python
#coding:utf-8
#from settings import config
from sqlalchemy.orm import scoped_session,sessionmaker
from models import engine
from settings import log
import models


session = scoped_session(sessionmaker(bind=engine,autocommit=False, autoflush=False))
def get_db():
    return session()

POLICY_MONTH = 0
POLICY_TIMING = 1


STAT_AUTH_ALL = 'STAT_AUTH_ALL'
STAT_AUTH_ACCEPT = 'STAT_AUTH_ACCEPT'
STAT_AUTH_REJECT = 'STAT_AUTH_REJECT'
STAT_AUTH_DROP = 'STAT_AUTH_DROP'
STAT_ACCT_ALL = 'STAT_ACCT_ALL'
STAT_ACCT_START = 'STAT_ACCT_START'
STAT_ACCT_UPDATE = 'STAT_ACCT_UPDATE'
STAT_ACCT_STOP = 'STAT_ACCT_STOP'
STAT_ACCT_ON = 'STAT_ACCT_ON'
STAT_ACCT_OFF = 'STAT_ACCT_OFF'
STAT_ACCT_DROP = 'STAT_ACCT_DROP'
STAT_ACCT_RETRY = 'STAT_ACCT_RETRY'


def incr_stat(name):
    db = get_db()
    try:
        statdata = db.query(models.RadStat).get(name)
        if not statdata:
            statdata = models.RadStat()
            statdata.name = name
            statdata.value = 1
            db.add(statdata)
        else:
            statdata.value = statdata.value + 1
        db.commit()
        db.flush()
    except Exception, e:
        log.error("update stat data error: %s"%str(e))
        db.rollback()


def get_stat(name):
    db = get_db()
    try:
        statdata = db.query(models.RadStat).get(name)
        if not statdata:
            return 0
        else:
            return statdata.value
    except Exception, e:
        log.error("query stat data error: %s"%str(e))
        return 0

def in_black_roster(macaddr):
    return False

def get_nas(ipaddr):
    return get_db().query(models.RadNas).filter_by(ip_addr = ipaddr).first()

def get_nas_ips(node_id):
    return[ nn.ip_addr  for nn in get_db().query(models.RadNasNode).filter_by(node_id = node_id)]

def user_exists(username):
    return get_db().query(models.RadUser).filter_by(user_name = username).count() > 0

def get_user(username):
    return get_db().query(models.RadUser).filter_by(user_name = username).first()

def set_user_mac(user_id,macaddr):
    db = get_db()
    try:
        user = get_db().query(models.RadUser).get(user_id)
        user.mac_addr = macaddr
        db.commit()
        db.flush()
    except Exception, e:
        log.error("set_user_mac error: %s"%str(e))
        db.rollback()

def set_user_vlanid(user_id,vlanid):
    db = get_db()
    try:
        user = get_db().query(models.RadUser).get(user_id)
        user.vlan_id = vlanid
        db.commit()
        db.flush()
    except Exception, e:
        log.error("set_user_vlanid error: %s"%str(e))
        db.rollback()

def set_user_vlanid2(user_id,vlanid2):
    db = get_db()
    try:
        user = get_db().query(models.RadUser).get(user_id)
        user.vlan_id2 = vlanid2
        db.commit()
        db.flush()
    except Exception, e:
        log.error("set_user_vlanid2 error: %s"%str(e))
        db.rollback()

def get_product(pid):
    return get_db().query(models.RadProduct).get(pid)

def get_online_num(username):
    return 0