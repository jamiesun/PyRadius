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
            areas = get_db().query(models.RadArea)\
             .filter(models.RadArea.node_id == node_id).all()
        else:
            areas = get_db().query(models.RadArea).all()
        return render("area.html",nodes=nodes,node_id=node_id,areas=areas)   

@app.route("/delete")
class index():
    def GET(self):
        node_id = web.input().get("node_id")
        area_id = web.input().get("area_id")
        if node_id and area_id:
            db = get_db()
            try:
                for area in db.query(models.RadArea)\
                 .filter(models.RadArea.node_id == node_id)\
                 .filter(models.RadArea.area_id == area_id):
                    db.delete(area)
                db.commit()
                db.flush()
            except Exception as e:
                db.rollback()
                log.error("delete area error: %s"%str(e))
                return errorpage("删除失败")
        raise web.seeother("/area",absolute=True)                

@app.route("/add")
class index():
    def GET(self):
        web.header("Content-Type","text/html; charset=utf-8")
        form = forms.area_add_form()
        form.fill(web.input())
        return render("baseform.html",form=form,title="新增区域",action="/area/add")   

    def POST(self):
        web.header("Content-Type","text/html; charset=utf-8")
        form = forms.area_add_form()
        if not form.validates(): 
            return render("baseform.html",form=form,title="新增区域",action="/area/add")    
        else:
            db = get_db()
            if db.query(models.RadArea)\
                 .filter(models.RadArea.node_id == form.d.node_id)\
                 .filter(models.RadArea.area_id == form.d.area_id)\
                 .count()>0:
                return errorpage("区域编码重复")       
            try:
                area = models.RadArea()
                area.node_id = form.d.node_id
                area.area_id = form.d.area_id
                area.area_name = form.d.area_name
                db.add(area)
                db.commit()
                db.flush()
            except Exception,e:
                db.rollback()
                log.error("add area error: %s"%str(e))
                return errorpage("新增区域失败 %s"%str(e))
            raise web.seeother("/area",absolute=True)

@app.route("/update")
class index():
    def GET(self):
        web.header("Content-Type","text/html; charset=utf-8")
        node_id = web.input().get("node_id")
        area_id = web.input().get("area_id")
        db = get_db()
        area = db.query(models.RadArea)\
                 .filter(models.RadArea.node_id == node_id)\
                 .filter(models.RadArea.area_id == area_id).first()
        form = forms.area_update_form()
        form.fill(area)
        return render("baseform.html",form=form,title="修改区域",action="/area/update")   

    def POST(self):
        web.header("Content-Type","text/html; charset=utf-8")
        form = forms.area_update_form()
        if not form.validates(): 
            return render("baseform.html",form=form,title="修改区域",action="/area/update")    
        else:
            db = get_db()
            area = db.query(models.RadArea)\
                 .filter(models.RadArea.node_id == form.d.node_id)\
                 .filter(models.RadArea.area_id == form.d.area_id).first()
            if not area:
                return errorpage("区域不存在")       
            try:
                area.area_name = form.d.area_name
                db.commit()
                db.flush()
            except Exception,e:
                db.rollback()
                log.error("update area error: %s"%str(e))
                return errorpage("修改区域失败 %s"%str(e))
            raise web.seeother("/area",absolute=True)

