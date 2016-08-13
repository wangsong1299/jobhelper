#!/usr/bin/python2.7 
# -*- coding: utf-8 -*-
import redis
import re
import time, datetime
import sys   #引用sys模块进来，并不是进行sys的第一次加载  
reload(sys)  #重新加载sys  
sys.setdefaultencoding('utf8')  ##调用setdefaultencoding函数

def checkMessage(func):
    def validate(self, user, message = ''):
        print user, message
        return func(self, user, message)
    return validate

class HrStatus:
    # need connect redis
    status_map = {
        '0': u'start',
        '1': u'请输入职位名称:',
        '2': u'请输入公司名称:',
        '3': u'请输入薪资范围:',
        '4': u'请输入学历要求:',
        '5': u'请输入工作年限:',
        '6': u'请输入性别:',
        '7': u'请输入公司地址:',
        '8': u'请输入职位描述，以分号分隔:'
    }
    
    def __init__(self, host = '183.136.128.100', port = 63794, db = 0, auth = 'gupiaocelve'):
        self.rConn = redis.Redis(host = host, port = port, db = db, password = auth)
##        print self.rConn.info()
        print 'redis connected!'
        
    def destroy(self):
        self.rConn.shutdown()
        print 'redis disconnected!'

    def validateInput(self, status, message = ""):
        if status == '6':
            if (message != 'male') and (message != '女'):
                return [False, u'性别请输入男或女']
        return [True, '']
        
    def setStatus(self, user, message = ''):
        rds_key = 'jobhelper_hunter_%s' % unicode(user)
        rds_info = 'jobhelper_hunter_info_%s' % unicode(user)
        print 'wss'
        
        if message == 'reset':
            self.rConn.set(rds_key, 0)
        else:
            self.rConn.setnx(rds_key, 0)
        status = self.rConn.get(rds_key) # 前状态
        [valid, tip] = self.validateInput(status, message)
        print status, message
        if valid:
            if int(status) > 0:
                self.rConn.hset(rds_info, status, message)
                self.rConn.expire(rds_info, 1800)
            self.rConn.incrby(rds_key, 1)
            status = unicode(int(status) + 1) # 后状态
            if status not in self.status_map:
                self.rConn.delete(rds_key)
                self.rConn.expire(rds_info, 300)
                tip = 'over'
            else:
                tip = self.status_map[status]
                self.rConn.expire(rds_key, 1200)
        else:
            self.rConn.expire(rds_key, 1200)
        return tip

    def getInfo(self, user):
        rds_info = 'jobhelper_hunter_info_%s' % unicode(user)
        if self.rConn:
            return self.rConn.hgetall(rds_info)
        return {}


rds = HrStatus(host = '127.0.0.1', port = 6379, auth = '')


    

    
