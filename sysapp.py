#!/usr/bin/env python
#coding:utf-8
from __future__ import unicode_literals  
from utils import route_app
from utils import render
import web
import forms


app  = route_app()

@app.route("")
class routeto():
    def GET(self):
        raise web.seeother("/sys/node",absolute=True)

@app.route("/node")
class index():
    def GET(self):
        web.header("Content-Type","text/html; charset=utf-8")
        return render("node.html") 


@app.route("/node/add")
class index():
    """ 节点管理 """
    def GET(self):
        web.header("Content-Type","text/html; charset=utf-8")
        form = forms.node_add_form()
        return render("baseform.html",form=form,title="新增节点",action="/sys/node/add")   

    def POST(self):
        web.header("Content-Type","text/html; charset=utf-8")
        form = forms.node_add_form()
        if not form.validates(): 
            return render("baseform.html",form=form,title="新增节点",action="/sys/node/add")   
        else:
            # form.d.boe and form['boe'].value are equivalent ways of
            # extracting the validated arguments from the form.
            return "ok"   

@app.route("/nas")
class index():
    def GET(self):
        web.header("Content-Type","text/html; charset=utf-8")
        return render("nas.html")             

@app.route("/nas/add")
class index():
    """ 节点管理 """
    def GET(self):
        web.header("Content-Type","text/html; charset=utf-8")
        form = forms.nas_add_form()
        return render("baseform.html",form=form,title="新增NAS设备",action="/sys/nas/add")   

    def POST(self):
        web.header("Content-Type","text/html; charset=utf-8")
        form = forms.nas_add_form()
        if not form.validates(): 
            return render("baseform.html",form=form,title="新增NAS设备",action="/sys/nas/add")    
        else:
            # form.d.boe and form['boe'].value are equivalent ways of
            # extracting the validated arguments from the form.
            return "ok"           


@app.route("/product")
class index():
    def GET(self):
        web.header("Content-Type","text/html; charset=utf-8")
        return render("product.html")             

@app.route("/product/add")
class index():
    """ 产品管理 """
    def GET(self):
        web.header("Content-Type","text/html; charset=utf-8")
        form = forms.product_add_form()
        return render("baseform.html",form=form,title="新增产品套餐",action="/sys/product/add")   

    def POST(self):
        web.header("Content-Type","text/html; charset=utf-8")
        form = forms.product_add_form()
        if not form.validates(): 
            return render("baseform.html",form=form,title="新增产品套餐",action="/sys/product/add")    
        else:
            # form.d.boe and form['boe'].value are equivalent ways of
            # extracting the validated arguments from the form.
            return "ok"                     