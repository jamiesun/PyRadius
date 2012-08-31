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
        products = get_db().query(models.RadProduct).all()
        return render("product.html",products=products)             

@app.route("/add")
class index():
    """ 产品管理 """
    def GET(self):
        web.header("Content-Type","text/html; charset=utf-8")
        form = forms.product_add_form()
        return render("baseform.html",form=form,title="新增产品套餐",action="/product/add")   

    def POST(self):
        web.header("Content-Type","text/html; charset=utf-8")
        form = forms.product_add_form()
        if not form.validates(): 
            return render("baseform.html",form=form,title="新增产品套餐",action="/product/add")    
        else:
            db = get_db()
            if db.query(models.RadProduct).filter(models.RadProduct.id == form.d.id).count()>0:
                return errorpage("产品编号重复")
            try:
                radproduct = models.RadProduct()
                radproduct.id = form.d.id
                radproduct.node_id = form.d.node_id
                radproduct.name = form.d.name
                radproduct.policy = form.d.policy
                radproduct.fee_num = form.d.fee_num
                radproduct.fee_price = form.d.fee_price
                radproduct.concur_number = form.d.concur_number
                radproduct.bind_mac = form.d.bind_mac
                radproduct.bind_vlan = form.d.bind_vlan
                radproduct.bandwidth_code = form.d.bandwidth_code
                radproduct.input_max_limit = form.d.input_max_limit
                radproduct.output_max_limit = form.d.output_max_limit
                radproduct.input_rate_code = form.d.input_rate_code
                radproduct.output_rate_code = form.d.output_rate_code
                radproduct.domain_code = form.d.domain_code
                radproduct.status = 0
                db.add(radproduct)
                db.commit()
            except Exception,e:
                return errorpage("产品新增失败 %s"%str(e))

            raise web.seeother("/product",absolute=True)             