#!/usr/bin/env python
#coding:utf-8
#from settings import config
from sqlalchemy.orm import scoped_session,sessionmaker
from caches import online_cache,user_cache,cache_data,stat_cache
from models import engine
from settings import radiuslog
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
    if stat_cache.has_key(name):
        stat_cache[name] += 1
    else:
        stat_cache[name] = 1


def get_stat(name):
    return stat_cache.get(name,0)


def in_black_roster(macaddr):
    return False

@cache_data()
def get_nas_all():
    return get_db().query(models.RadNas).all()

@cache_data()
def get_nas(ipaddr):
    return get_db().query(models.RadNas).filter_by(ip_addr = ipaddr).first()

@cache_data()
def get_nas_ips(node_id):
    return [ nn.ip_addr  for nn in get_db().query(models.RadNasNode).filter_by(node_id = node_id)]

def user_exists(username):
    return get_user(username) is not None

def get_user(username):
    user = user_cache.get(username)
    if not user:
        user = get_db().query(models.RadUser).filter_by(user_name = username).first()
        if user:
            user_cache[username] = user
    return user

def update_user_balance(username,balance):
    db = get_db()
    user = db.query(models.RadUser).filter_by(user_name = username).first()
    user.balance = balance
    db.commit()
    db.flush()
    user_cache[username] = user


def set_user_mac(username,macaddr):
    user = get_user(username)
    if user:
        user.mac_addr = macaddr
    # db = get_db()
    # try:
    #     user = get_db().query(models.RadUser).get(user_id)
    #     user.mac_addr = macaddr
    #     db.commit()
    #     db.flush()
    #     user_cache[user.user_name] = user
    # except Exception, e:
    #     radiuslog.error("set_user_mac error: %s"%str(e))
    #     db.rollback()

def set_user_vlanid(username,vlanid):
    user = get_user(username)
    if user:    
        user.vlan_id = vlanid
    # db = get_db()
    # try:
    #     user = get_db().query(models.RadUser).get(user_id)
    #     user.vlan_id = vlanid
    #     db.commit()
    #     db.flush()
    #     user_cache[user.user_name] = user
    # except Exception, e:
    #     radiuslog.error("set_user_vlanid error: %s"%str(e))
    #     db.rollback()

def set_user_vlanid2(username,vlanid2):
    user = get_user(username)
    if user:    
        user.vlan_id2 = vlanid2  
    # db = get_db()
    # try:
    #     user = get_db().query(models.RadUser).get(user_id)
    #     user.vlan_id2 = vlanid2
    #     db.commit()
    #     db.flush()
    #     user_cache[user.user_name] = user
    # except Exception, e:
    #     radiuslog.error("set_user_vlanid2 error: %s"%str(e))
    #     db.rollback()

@cache_data()
def get_product(pid):
    return get_db().query(models.RadProduct).get(pid)

def get_online(key):
    return online_cache.get(key)

def get_online_keys():
    return online_cache.keys()

def is_online(olkey):
    return online_cache.has_key(olkey)

def get_online_num(username):
    return len(online_cache)

def add_online(key,value):
    online_cache[key] = value

def rmv_online(key):
    return online_cache.pop(key,None)

