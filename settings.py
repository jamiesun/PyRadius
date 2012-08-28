#!/usr/bin/env python
#coding:utf-8

import logging,sys

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

log = getLogger("info","info.log")