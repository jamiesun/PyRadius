#!/usr/bin/env python
#coding:utf-8
import sys
import logging

def getLogger(name,logfile,level=logging.DEBUG):
    formatter = logging.Formatter('%(name)-12s %(asctime)s %(levelname)-8s %(message)s', '%a, %d %b %Y %H:%M:%S',)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    file_handler = logging.FileHandler(logfile)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    if level == logging.DEBUG:
        stream_handler = logging.StreamHandler(sys.stderr)
        logger.addHandler(stream_handler)   
    return logger


config = {
  "portalUrl":"",#推出Portal信息portal(port,url,ip)
  "rejectDelay":9,#认证拒绝达到7次,该用户将启动拒绝延迟,以缓慢DOS/穷举攻击,单位:秒,0表示不延迟,最大9秒
}

radiuslog = getLogger("pyradius","radius.log",level=logging.DEBUG)
ticketlog = getLogger("pyradius","ticket.log",level=logging.INFO)


vendor_cfg = {
  2011:{ # huawei
      "filter_id":'',
      "context":'',
      "input_max_limit":'Huawei-Input-Peak-Rate',
      "output_max_limit":'Huawei-Output-Peak-Rate',
      "input_rate_code":'',
      "output_rate_code":''
  }

} 