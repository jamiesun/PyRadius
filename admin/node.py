#!/usr/bin/env python
#coding:utf-8
from __future__ import unicode_literals  
from utils import route_app
from utils import render
from utils import nextid
from utils import get_db
from utils import errorpage
from utils import encrypt
from utils import decrypt
from settings import log
import web
import forms
import models


app  = route_app()

@app.route("")
class routeto():
    def GET(self):
        web.header("Content-Type","text/html; charset=utf-8")
        nodes = get_db().query(models.RadNode).all()
        return render("node.html",nodes=nodes) 

@app.route("/delete/(.*)")
class index():
    """删除节点及节点下的操作员"""
    def GET(self,nodeid):
        if nodeid:
            db = get_db()
            try:
                for node in db.query(models.RadNode).filter(models.RadNode.id == nodeid):
                    db.delete(node)
                for opr in db.query(models.RadOpr).filter(models.RadOpr.node_id == nodeid):
                    db.delete(opr)   
                for nasnode in db.query(models.RadNasNode).filter(models.RadNasNode.node_id == nodeid):
                    db.delete(nasnode)                     
                db.commit()
                db.flush()
            except Exception,e:
                db.rollback()
                log.error("delete node error: %s"%str(e))
                return errorpage("删除失败 %s"%str(e))
        raise web.seeother("/node",absolute=True)

@app.route("/add")
class index():
    """ 节点新增 """
    def GET(self):
        web.header("Content-Type","text/html; charset=utf-8")
        form = forms.node_add_form()
        return render("baseform.html",form=form,title="新增节点",action="/node/add")   

    def POST(self):
        web.header("Content-Type","text/html; charset=utf-8")
        form = forms.node_add_form()
       
        if not form.validates(source=web.input(nas_bind=[])): 
            return render("baseform.html",form=form,title="新增节点",action="/node/add")   
        else:
            db = get_db()
            if db.query(models.RadNode).filter(models.RadNode.id == form.d.node_id).count()>0:
                return errorpage("节点编号重复")
            try:
                radnode = models.RadNode()
                radnode.id = form.d.node_id
                radnode.name = form.d.node_name
                radnode.desc = form.d.node_desc

                radopr = models.RadOpr()
                radopr.node_id = radnode.id
                radopr.id = nextid()
                radopr.type = 1
                radopr.name = form.d.opr_name
                radopr.ip_addr = form.d.opr_ip
                radopr.password = encrypt(form.d.opr_passwd)
                radopr.status = 0

                db.add(radnode)
                db.add(radopr)


                #新增nas绑定
                for ip in form.d.nas_bind:
                    radnasnode = models.RadNasNode()
                    radnasnode.node_id = radnode.id
                    radnasnode.ip_addr = ip
                    db.add(radnasnode) 

                db.commit()
                db.flush()
            except Exception,e:
                db.rollback()
                log.error("add node error: %s"%str(e))
                return errorpage("节点新增失败 %s"%str(e))

            raise web.seeother("/node",absolute=True)


@app.route("/update/(.*)")
class index():
    """ 节点修改"""
    def GET(self,nodeid):
        web.header("Content-Type","text/html; charset=utf-8")
        db = get_db()
        radnode = db.query(models.RadNode).get(nodeid)
        radopr = db.query(models.RadOpr)\
            .filter(models.RadOpr.type==1)\
            .filter(models.RadOpr.node_id == nodeid).first() 
        nodenas = db.query(models.RadNasNode)\
            .filter(models.RadNasNode.node_id == nodeid)
        data = dict(node_id=radnode.id,
            node_name=radnode.name,
            node_desc=radnode.desc,
            opr_id=radopr.id,
            opr_name=radopr.name,
            opr_ip=radopr.ip_addr,
            opr_passwd=decrypt(radopr.password),
            nas_bind=[ nn.ip_addr for nn in nodenas ])  
        form = forms.node_update_form()
        form.fill(data)
        return render("baseform.html",form=form,title="修改节点",action="/node/update/")   

    def POST(self,none):
        web.header("Content-Type","text/html; charset=utf-8")
        form = forms.node_update_form()
        if not form.validates(source=web.input(nas_bind=[])): 
            return render("baseform.html",form=form,title="新增节点",action="/node/update/")   
        else:
            db = get_db()
            radnode = db.query(models.RadNode).filter(models.RadNode.id == form.d.node_id).first()
            if not radnode:
                return errorpage("节点不存在")

            try:
                radnode.id = form.d.node_id
                radnode.name = form.d.node_name
                radnode.desc = form.d.node_desc

                radopr = db.query(models.RadOpr)\
                .filter(models.RadOpr.type==1)\
                .filter(models.RadOpr.node_id == form.d.node_id).first()
                radopr.node_id = radnode.id
                radopr.id = nextid()
                radopr.type = 1
                radopr.name = form.d.opr_name
                radopr.ip_addr = form.d.opr_ip
                radopr.password = encrypt(form.d.opr_passwd)
                radopr.status = 0

                #修改nas绑定
                for nasnode in db.query(models.RadNasNode).filter(models.RadNasNode.node_id == radnode.id):
                    db.delete(nasnode)

                for ip in form.d.nas_bind:
                    radnasnode = models.RadNasNode()
                    radnasnode.node_id = radnode.id
                    radnasnode.ip_addr = ip
                    db.add(radnasnode) 

                db.commit()
                db.flush()
            except Exception,e:
                db.rollback()
                log.error("update node error: %s"%str(e))
                return errorpage("节点修改失败 %s"%str(e))
            raise web.seeother("/node",absolute=True)


