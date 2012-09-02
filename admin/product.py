#!/usr/bin/env python
#coding:utf-8
from __future__ import unicode_literals  
from utils import route_app
from utils import render
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
                db.flush()
            except Exception,e:
                db.rollback()
                return errorpage("产品新增失败 %s"%str(e))

            raise web.seeother("/product",absolute=True)             


@app.route("/update/(.*)")
class index():
    def GET(self,productid):
        web.header("Content-Type","text/html; charset=utf-8")
        form = forms.product_update_form()
        db = get_db()
        product = db.query(models.RadProduct).get(productid)
        form.fill(product)
        return render("baseform.html",form=form,title="修改产品套餐",action="/product/update/")   

    def POST(self,none):
        web.header("Content-Type","text/html; charset=utf-8")
        form = forms.product_update_form()
        if not form.validates(): 
            return render("baseform.html",form=form,title="修改产品套餐",action="/product/update/")    
        else:
            db = get_db()
            product = db.query(models.RadProduct).get(form.d.id)
            if not product:
                return errorpage("产品不存在")
            try:
                product.name = form.d.name
                product.fee_num = form.d.fee_num
                product.fee_price = form.d.fee_price
                product.concur_number = form.d.concur_number
                product.bind_mac = form.d.bind_mac
                product.bind_vlan = form.d.bind_vlan
                product.bandwidth_code = form.d.bandwidth_code
                product.input_max_limit = form.d.input_max_limit
                product.output_max_limit = form.d.output_max_limit
                product.input_rate_code = form.d.input_rate_code
                product.output_rate_code = form.d.output_rate_code
                product.domain_code = form.d.domain_code
                product.status = 0
                db.commit()
                db.flush()
            except Exception,e:
                db.rollback()
                return errorpage("修改新增失败 %s"%str(e))

            raise web.seeother("/product",absolute=True) 


@app.route("/delete/(.*)")
class index():
    def GET(self,productid):
        if productid:
            db = get_db()
            try:
                if db.query(models.RadUser).filter(models.RadUser.product_id == productid).count()>0:
                    return errorpage("产品已经有用户使用，不允许删除")
                radproduct = db.query(models.RadProduct).get(productid)
                if radproduct:
                    db.delete(radproduct)                     
                    db.commit()
                    db.flush()
            except Exception,e:
                db.rollback()
                return errorpage("删除失败 %s"%str(e))
        raise web.seeother("/product",absolute=True)   