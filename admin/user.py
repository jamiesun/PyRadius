#!/usr/bin/env python
#coding:utf-8
from __future__ import unicode_literals  
from utils import route_app
from utils import render
from utils import get_db
from utils import errorpage
from utils import nextid
from utils import encrypt
from utils import decrypt
from utils import currtime
from settings import log
import web
import forms
import models


app  = route_app()

@app.route("")
class routeto():
    def GET(self):
        web.header("Content-Type","text/html; charset=utf-8")
        node_id = web.input().get("node_id")
        nodes = get_db().query(models.RadNode).all()
        if node_id:
            users = get_db().query(models.RadUser)\
             .filter(models.RadUser.node_id == node_id).all()
        else:
            users = get_db().query(models.RadUser).all()
        return render("user.html",nodes=nodes,node_id=node_id,users=users)   

@app.route("/delete")
class index():
    def GET(self):
        user_id = web.input().get("user_id")
        if user_id:
            db = get_db()
            try:
                for user in db.query(models.RadUser).filter(models.RadUser.id == user_id):
                    db.delete(user)
                db.commit()
                db.flush()
            except Exception as e:
                db.rollback()
                log.error("delete user error: %s"%str(e))
                return errorpage("删除失败")
        raise web.seeother("/user",absolute=True)

def getAreaCommunity(node_id):
    ac_results = []
    db = get_db()
    areas = db.query(models.RadArea).filter(models.RadArea.node_id==node_id)
    for area in areas:
        communitys = db.query(models.RadCommunity).filter(models.RadCommunity.area_id == area.area_id)
        cys = []
        for community in communitys:   
             cys.append(("%s,%s"%(area.area_id,community.community_id),community.community_name))
        ac_results.append((area.area_name,cys))
    return ac_results


@app.route("/add")
class index():
    def GET(self):
        web.header("Content-Type","text/html; charset=utf-8")
        node_id = web.input().get("node_id")
        form = forms.user_add_form()
        form.area_community.args = getAreaCommunity(node_id)
        form.node_id.set_value(node_id)
        return render("baseform.html",form=form,title="新增用户",action="/user/add")   

    def POST(self):
        web.header("Content-Type","text/html; charset=utf-8")
        form = forms.user_add_form()
        if not form.validates(): 
            form.area_community.args = getAreaCommunity(form.d.node_id)
            return render("baseform.html",form=form,title="新增用户",action="/user/add")    
        else:
            db = get_db()
            if db.query(models.RadUser)\
                 .filter(models.RadUser.user_name == form.d.user_name)\
                 .count()>0:
                return errorpage("帐号重复")       
            try:

                area_community = form.d.area_community
                attrs = area_community.split(",")
                area_id = attrs[0]
                community_id = attrs[1]

                user = models.RadUser()
                user.id = nextid()
                user.node_id = form.d.node_id
                user.area_id = area_id
                user.community_id = community_id
                user.user_name = form.d.user_name
                user.user_cname = form.d.user_cname
                user.password = encrypt(form.d.password)
                user.product_id = form.d.product_id
                user.status = form.d.status
                user.auth_begin_date = form.d.auth_begin_date
                user.auth_end_date = form.d.auth_end_date
                user.user_control = form.d.user_control
                user.concur_number = form.d.concur_number
                user.user_vlan = form.d.user_vlan
                user.user_mac = form.d.user_mac
                user.ip_addr = form.d.ip_addr
                user.install_address = form.d.install_address
                user.balance = 0
                user.time_length = 0
                user.basic_fee = 0
                user.create_time = currtime()
                db.add(user)
                db.commit()
                db.flush()
            except Exception,e:
                db.rollback()
                log.error("add user error: %s"%str(e))
                return errorpage("新增用户失败 %s"%str(e))
            raise web.seeother("/user",absolute=True)

@app.route("/update")
class index():
    def GET(self):
        web.header("Content-Type","text/html; charset=utf-8")
        user_id = web.input().get("user_id")
        db = get_db()
        user = db.query(models.RadUser).get(user_id)
        form = forms.user_update_form()
        form.fill(user)
        form.area_community.args = getAreaCommunity(user.node_id)
        form.area_community.value = "%s,%s"%(user.area_id,user.community_id)
        form.password.value = decrypt(user.password)
        return render("baseform.html",form=form,title="修改用户",action="/user/update")   

    def POST(self):
        web.header("Content-Type","text/html; charset=utf-8")
        form = forms.user_update_form()
        if not form.validates(): 
            form.area_community.args = getAreaCommunity(form.d.node_id)
            return render("baseform.html",form=form,title="修改用户",action="/user/update")    
        else:
            db = get_db()
            user = db.query(models.RadUser).get(form.d.id)
            if not user:
                return errorpage("用户不存在")       
            try:

                area_community = form.d.area_community
                attrs = area_community.split(",")
                area_id = attrs[0]
                community_id = attrs[1]

                user.area_id = area_id
                user.community_id = community_id
                user.user_cname = form.d.user_cname
                user.password = encrypt(form.d.password)
                user.product_id = form.d.product_id
                user.status = form.d.status
                user.auth_begin_date = form.d.auth_begin_date
                user.auth_end_date = form.d.auth_end_date
                user.user_control = form.d.user_control
                user.concur_number = form.d.concur_number
                user.user_vlan = form.d.user_vlan
                user.user_mac = form.d.user_mac
                user.ip_addr = form.d.ip_addr
                user.install_address = form.d.install_address
                # user.balance = 0
                # user.time_length = 0
                # user.basic_fee = 0
                # user.create_time = currtime()
                db.commit()
                db.flush()
            except Exception,e:
                db.rollback()
                log.error("update user error: %s"%str(e))
                return errorpage("修改用户失败 %s"%str(e))
            raise web.seeother("/user",absolute=True)



