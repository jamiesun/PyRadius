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
from Crypto.Cipher import AES
import binascii

_key = '___a_b_c_d_e_f__'

session = scoped_session(sessionmaker(bind=engine,autocommit=False, autoflush=False))()
def get_db():
    print "connection id:",id(session.connection)
    return session

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

def is_select(v1,v2):
    return  str(v1 or '') in str(v2 or '')  and "selected" or ""

def render(filename,**args):
    """ define mako render function """
    try:
        mytemplate = _lookup.get_template(filename) 
        args["sitename"] = config.get("sitename")
        args["cdate"] = datetime.datetime.now().strftime( "%Y-%m-%d")
        args['session'] = web.ctx.session 
        args["ctx"] = web.ctx
        args["current_css"] = current_css
        args["is_select"] = is_select
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

def encrypt(x):
    if not x:return ''
    x = str(x)
    result =  AES.new(_key, AES.MODE_CBC).encrypt(x.ljust(len(x)+(16-len(x)%16)))
    return binascii.hexlify(result)

def decrypt(x):
    if not x or len(x)%16 > 0 :return ''
    x = binascii.unhexlify(str(x))
    return AES.new(_key, AES.MODE_CBC).decrypt(x).strip()    



