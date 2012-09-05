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
        area_id = web.input().get("area_id")
        nodes = get_db().query(models.RadNode).all()
        for node in nodes:
            areas = get_db().query(models.RadArea)\
             .filter(models.RadArea.node_id == node.id).all()
            node.areas = areas        
        if node_id and area_id:
            communitys = get_db().query(models.RadCommunity)\
             .filter(models.RadCommunity.node_id == node_id)\
             .filter(models.RadCommunity.area_id == area_id)\
             .all()
        else:
            communitys = get_db().query(models.RadCommunity).all()
        return render("community.html",nodes=nodes,node_area="%s,%s"%(node_id,area_id),communitys=communitys)   

@app.route("/delete")
class index():
    def GET(self):
        node_id = web.input().get("node_id")
        area_id = web.input().get("area_id")
        community_id = web.input().get("community_id")
        if node_id and area_id and community_id:
            db = get_db()
            try:
                for community in db.query(models.RadCommunity)\
                 .filter(models.RadCommunity.node_id == node_id)\
                 .filter(models.RadCommunity.area_id == area_id)\
                 .filter(models.RadCommunity.community_id == community_id):
                    db.delete(community)
                db.commit()
                db.flush()
            except Exception as e:
                db.rollback()
                log.error("delete community error: %s"%str(e))
                return errorpage("删除失败")
        raise web.seeother("/community",absolute=True)                

@app.route("/add")
class index():
    def GET(self):
        web.header("Content-Type","text/html; charset=utf-8")
        form = forms.community_add_form()
        form.fill(web.input())
        return render("baseform.html",form=form,title="新增小区",action="/community/add")   

    def POST(self):
        web.header("Content-Type","text/html; charset=utf-8")
        form = forms.community_add_form()
        if not form.validates(): 
            return render("baseform.html",form=form,title="新增小区",action="/community/add")    
        else:
            db = get_db()
            if db.query(models.RadCommunity)\
                 .filter(models.RadCommunity.node_id == form.d.node_id)\
                 .filter(models.RadCommunity.area_id == form.d.area_id)\
                 .filter(models.RadCommunity.community_id == form.d.community_id)\
                 .count()>0:
                return errorpage("小区编码重复")       
            try:
                community = models.RadCommunity()
                community.node_id = form.d.node_id
                community.area_id = form.d.area_id
                community.community_id = form.d.community_id
                community.community_name = form.d.community_name
                db.add(community)
                db.commit()
                db.flush()
            except Exception,e:
                db.rollback()
                log.error("add community error: %s"%str(e))
                return errorpage("新增小区失败 %s"%str(e))
            raise web.seeother("/community",absolute=True)

@app.route("/update")
class index():
    def GET(self):
        web.header("Content-Type","text/html; charset=utf-8")
        node_id = web.input().get("node_id")
        area_id = web.input().get("area_id")
        community_id = web.input().get("community_id")
        db = get_db()
        community = db.query(models.RadCommunity)\
                 .filter(models.RadCommunity.node_id == node_id)\
                 .filter(models.RadCommunity.area_id == area_id)\
                 .filter(models.RadCommunity.community_id == community_id).first()
        form = forms.community_update_form()
        form.fill(community)
        return render("baseform.html",form=form,title="修改小区",action="/community/update")   

    def POST(self):
        web.header("Content-Type","text/html; charset=utf-8")
        form = forms.community_update_form()
        if not form.validates(): 
            return render("baseform.html",form=form,title="修改小区",action="/community/update")    
        else:
            db = get_db()
            community = db.query(models.RadCommunity)\
                 .filter(models.RadCommunity.node_id == form.d.node_id)\
                 .filter(models.RadCommunity.area_id == form.d.area_id)\
                 .filter(models.RadCommunity.community_id == form.d.community_id).first()
            if not community:
                return errorpage("小区不存在")       
            try:
                community.community_name = form.d.community_name
                db.commit()
                db.flush()
            except Exception,e:
                db.rollback()
                log.error("update community error: %s"%str(e))
                return errorpage("修改小区失败 %s"%str(e))
            raise web.seeother("/community",absolute=True)

