#!/usr/bin/env python
#coding:utf-8
from __future__ import unicode_literals  
from utils import route_app
from utils import render
from utils import nextid
from utils import get_db
from utils import errorpage
import web
import forms
import models


app  = route_app()

@app.route("")
class routeto():
    def GET(self):
        web.header("Content-Type","text/html; charset=utf-8")
        nass = get_db().query(models.RadNas).all()
        return render("nas.html",nass=nass)   

@app.route("/delete/(.*)")
class index():
    """删除Nas"""
    def GET(self,nasid):
        if nasid:
            db = get_db()
            try:
                for nas in db.query(models.RadNas).filter(models.RadNas.id == nasid):
                    db.delete(nas)
                db.commit()
            except:
                return errorpage("删除失败")
        raise web.seeother("/nas",absolute=True)                

@app.route("/add")
class index():
    """ Nas管理 """
    def GET(self):
        web.header("Content-Type","text/html; charset=utf-8")
        form = forms.nas_add_form()
        return render("baseform.html",form=form,title="新增NAS设备",action="/nas/add")   

    def POST(self):
        web.header("Content-Type","text/html; charset=utf-8")
        form = forms.nas_add_form()
        if not form.validates(): 
            return render("baseform.html",form=form,title="新增NAS设备",action="/nas/add")    
        else:
            db = get_db()
            if db.query(models.RadNas).filter(models.RadNas.ip_addr == form.d.ip_addr).count()>0:
                return errorpage("Nas %s 已经存在"%form.d.ip_addr)       
            try:
                nas = models.RadNas()
                nas.id = nextid()
                nas.ip_addr = form.d.ip_addr
                nas.name = form.d.name
                nas.auth_secret = form.d.auth_secret
                nas.acct_secret = form.d.acct_secret
                nas.vendor_id = form.d.vendor_id
                nas.time_type = form.d.time_type
                nas.status = form.d.status
                db.add(nas)
                db.commit()
            except:
                db.rollback()
                return errorpage("新增Nas失败")
            raise web.seeother("/nas",absolute=True)

@app.route("/update/(.*)")
class index():
    """ Nas管理 """
    def GET(self,nasid):
        web.header("Content-Type","text/html; charset=utf-8")
        db = get_db()
        nas = db.query(models.RadNas).get(nasid)
        data = dict(id=nas.id,
                ip_addr=nas.ip_addr,
                name=nas.name,
                auth_secret=nas.auth_secret,
                acct_secret=nas.acct_secret,
                vendor_id=nas.vendor_id,
                time_type=nas.time_type,
                status=nas.status)
        form = forms.nas_update_form()
        form.fill(data)
        return render("baseform.html",form=form,title="修改NAS设备",action="/nas/update/")   

    def POST(self,none):
        web.header("Content-Type","text/html; charset=utf-8")
        form = forms.nas_update_form()
        if not form.validates(): 
            return render("baseform.html",form=form,title="修改NAS设备",action="/nas/update/")    
        else:
            db = get_db()
            nas = db.query(models.RadNas).get(form.d.id)
            if not nas:
                return errorpage("Nas不存在")       
            try:
                nas.name = form.d.name
                nas.auth_secret = form.d.auth_secret
                nas.acct_secret = form.d.acct_secret
                nas.vendor_id = form.d.vendor_id
                nas.time_type = form.d.time_type
                nas.status = form.d.status
                db.commit()
            except:
                return errorpage("修改Nas失败")
            raise web.seeother("/nas",absolute=True)

