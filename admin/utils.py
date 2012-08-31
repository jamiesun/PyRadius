#!/usr/bin/env python
#coding:utf-8
from __future__ import unicode_literals  
import uuid
import datetime
import web
from mako.lookup import TemplateLookup 
from mako import exceptions
from beaker.cache import CacheManager
from settings import config
from sqlalchemy.orm import scoped_session,sessionmaker
from models import engine

session = scoped_session(sessionmaker(bind=engine))
def get_db():
    return session()

APP_DIR = "./"

""" 内存缓存配置 """
cache = CacheManager(cache_regions={
    'long_term':{
        'type': 'memory',
        'expire': 360000
    },
})
  

""" mako模板配置 """
_lookup = TemplateLookup(directories=['%s/templates'%APP_DIR],
                          input_encoding='utf-8',
                          output_encoding='utf-8',
                          encoding_errors='replace',
                          module_directory="%s/tmp"%APP_DIR,
                          cache_impl='beaker',
                          cache_args={'manager':cache } )  

def current_css(rpath):
    if  web.ctx.homepath and web.ctx.homepath in rpath:
        return 'current'
    else:
        return ""


def render(filename,**args):
    """ define mako render function """
    try:
        mytemplate = _lookup.get_template(filename) 
        args["sitename"] = config.get("sitename")
        args["cdate"] = datetime.datetime.now().strftime( "%Y-%m-%d")
        args['session'] = web.ctx.session 
        args["ctx"] = web.ctx
        args["current_css"] = current_css
        return mytemplate.render(**args)
    except:
        return exceptions.text_error_template().render()

def notfound():
    return web.notfound("Sorry, the page you were looking for was not found.")

def errorpage(msg,title="消息"):
    web.header("Content-Type","text/html; charset=utf-8")
    return render("error.html",error=msg,title=title)   

class route_app(web.application): 
    def mount(self,pattern,app):
        self.add_mapping(pattern, app)     
    def route(self, *args): 
        def wrapper(cls): 
            for pattern in args: 
                self.add_mapping(pattern, cls) 
            return cls 
        return wrapper

def nextid():
    return uuid.uuid4().hex

def currtime():
    return datetime.datetime.now().strftime( "%Y-%m-%d %H:%M:%S")

def encrypt(s,key=128):
    b = bytearray(str(s).encode("utf8"))
    n = len(b) 
    c = bytearray(n*2)
    j = 0
    for i in range(0, n):
        b1 = b[i]
        b2 = b1 ^ key 
        c1 = b2 % 16
        c2 = b2 // 16 
        c1 = c1 + 65
        c2 = c2 + 65 
        c[j] = c1
        c[j+1] = c2
        j = j+2
    return c.decode("utf8")

def decrypt(s,key=128):
    c = bytearray(str(s).encode("utf8"))
    n = len(c) 
    if n % 2 != 0 :
        return ""
    n = n // 2
    b = bytearray(n)
    j = 0
    for i in range(0, n):
        c1 = c[j]
        c2 = c[j+1]
        j = j+2
        c1 = c1 - 65
        c2 = c2 - 65
        b2 = c2*16 + c1
        b1 = b2^ key
        b[i]= b1
    try:
        return b.decode("utf8")
    except:
        return "failed"





