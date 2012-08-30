#!/usr/bin/env python
#coding:utf-8
import uuid
import datetime
import web
from mako.lookup import TemplateLookup 
from mako import exceptions
from beaker.cache import CacheManager
from settings import config

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
    fullpath = "%s%s"%(web.ctx.homepath,web.ctx.path)
    if rpath in fullpath:
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

def errorpage(msg):
    web.header("Content-Type","text/html; charset=utf-8")
    return render("error.html",error=msg)   

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