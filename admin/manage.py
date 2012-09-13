#!/usr/bin/env python
#coding:utf-8
# from gevent import monkey; monkey.patch_all()
# from gevent.wsgi import WSGIServer
from utils import route_app
from settings import config
from utils import render
import node
import group
import user
import nas
import product
import web


""" application defined """
app  = route_app()
app.mount("/node",node.app)
app.mount("/group",group.app)
app.mount("/nas",nas.app)
app.mount("/product",product.app)
app.mount("/user",user.app)

'''session defined'''
# session = web.session.Session(app, web.session.DiskStore('sessions'), {'count': 0})   
if web.config.get('_session') is None:
   session = web.session.Session(app, web.session.DiskStore('sessions'), {'count': 0})
   web.config._session = session
else:
   session = web.config._session

def context_hook():
    web.ctx.config = config
    web.ctx.session = session

app.add_processor(web.loadhook(context_hook))   

@app.route("/test")
class test():
    def GET(self):
        return "ok"



@app.route("/favicon.ico")
class js():
    def GET(self):
        raise web.seeother("/static/favicon.ico",absolute=True)

@app.route("/index")
class home():
    def GET(self):
        web.header("Content-Type","text/html; charset=utf-8")
        raise web.seeother("/",absolute=True)

@app.route("/scripts/(.*)")
class js():
    def GET(self,filename):
        raise web.seeother("/static/scripts/%s"%filename,absolute=True)

@app.route("/css/(.*)")
class css():
    def GET(self,filename):
        raise web.seeother("/static/css/%s"%filename,absolute=True)

@app.route("/images/(.*)")
class img():
    def GET(self,filename):
        raise web.seeother("/static/images/%s"%filename,absolute=True)    


@app.route("/")
class index():
    def GET(self):
        web.header("Content-Type","text/html; charset=utf-8")
        return render("index.html")

@app.route("/login")
class login():
    def GET(self):
        web.header("Content-Type","text/html; charset=utf-8")
        return render("login.html")         

    def POST(self):
        web.header("Content-Type","text/html; charset=utf-8")
        raise web.seeother("/",absolute=True)


web.config.debug = False

#wsgi run
#application = app.wsgifunc()    


if __name__ == "__main__":
    import  platform
    if  platform.system() == "Windows":
        web.config.debug = False
        #WSGIServer(('', 8080), application,log=None).serve_forever()
        app.run()