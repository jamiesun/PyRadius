#!/usr/bin/env python
#coding:utf-8
from __future__ import unicode_literals  
import sys
import logging

def getLogger(name,logfile,level=logging.DEBUG):
    formatter = logging.Formatter('%(name)-12s %(asctime)s %(levelname)-8s %(message)s', '%a, %d %b %Y %H:%M:%S',)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    file_handler = logging.FileHandler(logfile)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    stream_handler = logging.StreamHandler(sys.stderr)
    if level == logging.DEBUG:
        logger.addHandler(stream_handler)   
    return logger


config = {
  "sitename":"radius manage",
  "pagesize":20,
  "portalUrl":"",#推出Portal信息portal(port,url,ip)
  "rejectDelay":9,#认证拒绝达到7次,该用户将启动拒绝延迟,以缓慢DOS/穷举攻击,单位:秒,0表示不延迟,最大9秒
}

log = getLogger("pyradius","info.log")

vendor_cfg = {
  3902:{ # zte
      "filter_id":'Filter-Id',
      "context":'',
      "input_max_limit":'',
      "output_max_limit":'',
      "input_rate_code":'',
      "output_rate_code":''
  }

} 