#!/usr/bin/env python
#coding:utf-8

from utils import route_app
from settings import config
from utils import render
import web

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
    def GET(self):
        web.header("Content-Type","text/html; charset=utf-8")
        return render("node_add.html")         