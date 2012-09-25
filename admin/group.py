#!/usr/bin/env python
#coding:utf-8
from __future__ import unicode_literals  
from utils import route_app
from utils import render
from utils import get_db
from utils import errorpage
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
            groups = get_db().query(models.RadGroup)\
             .filter(models.RadGroup.node_id == node_id).all()
        else:
            groups = get_db().query(models.RadGroup).all()
        return render("group.html",nodes=nodes,node_id=node_id,groups=groups)   

@app.route("/delete")
class index():
    def GET(self):
        node_id = web.input().get("node_id")
        group_id = web.input().get("group_id")
        if node_id and group_id:
            db = get_db()
            try:
                for group in db.query(models.RadGroup)\
                 .filter(models.RadGroup.node_id == node_id)\
                 .filter(models.RadGroup.group_id == group_id):
                    db.delete(group)
                db.commit()
                db.flush()
            except Exception as e:
                db.rollback()
                log.error("delete group error: %s"%str(e))
                return errorpage("删除失败")
        raise web.seeother("/group",absolute=True)                

@app.route("/add")
class index():
    def GET(self):
        web.header("Content-Type","text/html; charset=utf-8")
        form = forms.group_add_form()
        form.fill(web.input())
        return render("baseform.html",form=form,title="新增用户组",action="/group/add")   

    def POST(self):
        web.header("Content-Type","text/html; charset=utf-8")
        form = forms.group_add_form()
        if not form.validates(): 
            return render("baseform.html",form=form,title="新增用户组",action="/group/add")    
        else:
            db = get_db()
            if db.query(models.RadGroup)\
                 .filter(models.RadGroup.node_id == form.d.node_id)\
                 .filter(models.RadGroup.group_id == form.d.group_id)\
                 .count()>0:
                return errorpage("用户组编码重复")       
            try:
                group = models.RadGroup()
                group.node_id = form.d.node_id
                group.group_id = form.d.group_id
                group.group_name = form.d.group_name
                db.add(group)
                db.commit()
                db.flush()
            except Exception,e:
                db.rollback()
                log.error("add group error: %s"%str(e))
                return errorpage("新增用户组失败 %s"%str(e))
            raise web.seeother("/group",absolute=True)

@app.route("/update")
class index():
    def GET(self):
        web.header("Content-Type","text/html; charset=utf-8")
        node_id = web.input().get("node_id")
        group_id = web.input().get("group_id")
        db = get_db()
        group = db.query(models.RadGroup)\
                 .filter(models.RadGroup.node_id == node_id)\
                 .filter(models.RadGroup.group_id == group_id).first()
        form = forms.group_update_form()
        form.fill(group)
        return render("baseform.html",form=form,title="修改用户组",action="/group/update")   

    def POST(self):
        web.header("Content-Type","text/html; charset=utf-8")
        form = forms.group_update_form()
        if not form.validates(): 
            return render("baseform.html",form=form,title="修改用户组",action="/group/update")    
        else:
            db = get_db()
            group = db.query(models.RadGroup)\
                 .filter(models.RadGroup.node_id == form.d.node_id)\
                 .filter(models.RadGroup.group_id == form.d.group_id).first()
            if not group:
                return errorpage("用户组不存在")       
            try:
                group.group_name = form.d.group_name
                db.commit()
                db.flush()
            except Exception,e:
                db.rollback()
                log.error("update group error: %s"%str(e))
                return errorpage("修改用户组失败 %s"%str(e))
            raise web.seeother("/group",absolute=True)

