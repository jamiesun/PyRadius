#!/usr/bin/env python
#coding:utf-8

import MySQLdb
from DBUtils.PooledDB import PooledDB
from sqlbean.db import connection

dbpool = PooledDB(creator=MySQLdb,
                    maxusage=1000,
                    host='localhost',
                    user='root',
                    passwd='root',
                    db='pyradius',
                    charset="utf8")

DATABASE = dbpool.connection()
DATABASE.b_commit = True

def get_db_by_table(table_name):
    return DATABASE

connection.get_db_by_table = get_db_by_table

from sqlbean.shortcut import Model

def todict(row,rowdesc):
    d = {}
    for idx, col in enumerate(rowdesc):
        d[col[0]] = row[idx]
    return d



class RadNode(Model):
    """节点
    """    
    class Meta:
        table="rad_node"

class RadNas(Model):
    """接入服务器
    """        
    class Meta:
        table="rad_nas"        

class RadNasNode(Model):
    """接入服务器与节点绑定
    """        
    class Meta:
        table="rad_nas_node"            

class RadOpr(Model):
    """操作员
    """        
    class Meta:
        table="rad_opr"        

class RadOprLog(Model):
    """操作日志
    """        
    class Meta:
        table="rad_opr_log"              

class RadUser(Model):
    """用户
    """        
    class Meta:
        table="rad_user"

class RadUserGroup(Model):
    """用户组
    """        
    class Meta:
        table="rad_user_group"       

class RadRoster(Model):
    """用户黑白名单
    """        
    class Meta:
        table="rad_roster"       

class RadProduct(Model):
    """业务套餐
    """        
    class Meta:
        table="rad_product" 

class RadUserOrder(Model):
    """用户订购套餐记录
    """        
    class Meta:
        table="rad_user_order" 

class RadUserAcct(Model):
    """用户实时计费
    """        
    class Meta:
        table="rad_user_acct" 

class RadUserBill(Model):
    """用户账单
    """        
    class Meta:
        table="rad_user_bill" 