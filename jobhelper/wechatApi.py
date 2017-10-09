#! /usr/bin/env python
# coding=utf-8

import xmltodict
import json, hashlib
import time, datetime
import urllib, urllib2
import ssl, socket
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class WechatApi:
    def __init__(self):
        # 开发者私有配置信息
        self.Token = 'job'
        self.EncodingAESKey = ''
        # 测试号码
        self.AppID = 'wxa4dea5931c6dc2ab'   # 开发者平台分配的AppID
        self.AppSecret = '74c146f361f1dc2991764fc667222b6a'

        # 使用微信接口获得的信息
        self.AccessToken = '' # 公众号的access_token
        self.ExpiresTime = time.time()
        self.IpList = [] # 公众号可信任ip
    
    def xmlToJson(self, xml):
        convertedDict = xmltodict.parse(xml)
        jsonStr = json.dumps(convertedDict, indent=1)
        jsonObj = json.loads(jsonStr)
        return jsonObj

    def jsonToXml(self, dictVal):
        dictVal = { 'root': dictVal }
        convertedXml = xmltodict.unparse(dictVal)
        return convertedXml

    def jsonToReturnXml(self, dictVal):
        dictVal = self.formatJson(dictVal)
        dictVal = { 'xml': dictVal }
        convertedXml = xmltodict.unparse(dictVal).replace('&lt;', '<').replace('&gt;', '>')
        return convertedXml

    def formatJson(self, dictVal):
        resDict = {}
        for dictKey in dictVal:
            if isinstance(dictVal[dictKey], str) or isinstance(dictVal[dictKey], unicode):
                resDict[dictKey] = '<![CDATA[%s]]>' % dictVal[dictKey]
            elif isinstance(dictVal[dictKey], list) or isinstance(dictVal[dictKey], tuple):
                tmpList = []
                for i in range(dictVal[dictKey]):
                    tmpList.append(self.formatJson(dictVal[dictKey][i]))
                resDict[dictKey] = tmpList
            elif isinstance(dictVal[dictKey], dict):
                resDict[dictKey] = {}
                for i in dictVal[dictKey]:
                    resDict[dictKey][i] = self.formatJson(dictVal[dictKey][i])
            else:
                resDict[dictKey] = dictVal[dictKey]
        return resDict

    def reqHttpData(self, url, method = 'post', data = {}):
        params = urllib.urlencode(data)

        headers = {}
        if method == 'get':
            params = urllib.urlencode(data)
            url = url + '?' + params
            req = urllib2.Request(url, headers = headers)
            res_data = urllib2.urlopen(req)

        elif method == 'post':
            params = json.dumps(data, ensure_ascii = False)
            params = params.encode('UTF-8', 'ignore')

            url = url + '?access_token=' + self.AccessToken
            headers = {
                'Content-Type'  : 'application/json;charset=utf-8',
                'Content-Length': len(params)
            }
            req = urllib2.Request(url, params, headers = headers) 
            res_data = urllib2.urlopen(req)

            # req = urllib2.Request(url)
            # req.add_header('Content-Type', 'application/json;charset=utf-8')
            # req.add_header('Content-Length', len(params))
            # res_data = urllib2.urlopen(req, params)

        res = res_data.read()
        return res

    def postDataBySocket(self, host, path = '/', port = 80, data = {}):

        params = json.dumps(data, ensure_ascii = False)
        params = params

        request = ''; 
        request = request + "POST " + path + '?access_token=' + self.AccessToken + " HTTP/1.1\r\n";  
        request = request + "Host:" + host + "\r\n";   
        request = request + "Capplication/json;charset=utf-8\r\n";  
        request = request + "Content-length: " + str(len(params)) + "\r\n";  
        request = request + "Connection: close\r\n"; 
        request = request + "\r\n";
        request = request + unicode(params, 'utf-8') + "\r\n";   
        print request
        
        sock = ssl.wrap_socket(socket.socket());
        # sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.connect((host, port));
        sock.sendall(request);
        recv_data = sock.recv(4096);
        # print recv_data
        sock.close();
        if recv_data.rfind('}') > 0:
            braceStart = recv_data.find('{');
            braceEnd = recv_data.rfind('}');
            res = recv_data[braceStart : braceEnd + 1]
        else:
            res = recv_data
        return res


    def checkSignature(self, timestamp, nonce):
        tmpArray = []
        tmpArray.append(self.Token)
        tmpArray.append(timestamp)
        tmpArray.append(nonce)
        tmpArray = sorted(tmpArray)
        data = ''.join(tmpArray)
        return hashlib.sha1(data).hexdigest();
    
    def getAccessToken(self):
        if (self.AccessToken is not '') and (time.time() < self.ExpiresTime):
            return
        
        url = 'https://api.weixin.qq.com/cgi-bin/token'
        data= {
            'grant_type': 'client_credential',
            'appid': self.AppID,
            'secret': self.AppSecret
        }
        tokenObj = self.reqHttpData(url, method = 'get', data = data)
        tokenObj = json.loads(tokenObj)
        self.ExpiresTime = time.time() + tokenObj['expires_in']
        self.AccessToken = tokenObj['access_token']
        print 'refresh access_token:', self.AccessToken

    def getCallbackIP(self):
        self.getAccessToken()
        url = 'https://api.weixin.qq.com/cgi-bin/getcallbackip'
        data = {
            'access_token': self.AccessToken
    }
        resData = self.reqHttpData(url, 'get', data)
        return json.loads(resData)

    def getUserList(self, next_openid = ''):
        self.getAccessToken()
        url = 'https://api.weixin.qq.com/cgi-bin/user/get'
        data= {
            'access_token': self.AccessToken,
            'next_openid': next_openid
        }
        resData = self.reqHttpData(url, 'get', data)
        return json.loads(resData)

    def getUserInfo(self, openid = ''):
        self.getAccessToken()
        url = 'https://api.weixin.qq.com/cgi-bin/user/info'
        data= {
            'access_token': self.AccessToken,
            'openid': openid,
            'lang': 'zh_CN'
        }
        resData = self.reqHttpData(url, 'get', data)
        return json.loads(resData)
    
    def getUserInfoBatchget(self, user_list = []):
        self.getAccessToken()
        url = 'https://api.weixin.qq.com/cgi-bin/user/info/batchget'
        post_user_list = []
        for user in user_list:
            post_user_list.append({'openid': user, 'lang': 'zh-CN'})
        data= {
            'user_list': post_user_list
        }
        resData = self.reqHttpData(url, 'post', data)
        return json.loads(resData)

    def sendCustomMsg(self, openid, msg, msgtype = 'text'):
        self.getAccessToken()
        url = 'https://api.weixin.qq.com/cgi-bin/message/custom/send'
        data = {}
        if msgtype == 'text':
            data= {
                'touser': openid,
                'msgtype': msgtype,
                'text': {
                    'content': msg
                }
            }
        resData = self.reqHttpData(url, 'post', data)
        return json.loads(resData)

    def createMenu(self, button_list):
        self.getAccessToken()
        url = 'https://api.weixin.qq.com/cgi-bin/menu/create'
        host = 'api.weixin.qq.com'
        path = '/cgi-bin/menu/create'
        data= {
            'button': button_list
        }
        resData = self.reqHttpData(url, 'post', data)
        print resData
        # resData = self.postDataBySocket(host, path = path, port = 443, data = data)
        return json.loads(resData)

    def getMenu(self):
        self.getAccessToken()
        url = 'https://api.weixin.qq.com/cgi-bin/menu/get'
        data= {
            'access_token': self.AccessToken
        }
        resData = self.reqHttpData(url, 'get', data)
        return json.loads(resData)

    def deleteMenu(self):
        self.getAccessToken()
        url = 'https://api.weixin.qq.com/cgi-bin/menu/delete'
        data= {
            'access_token': self.AccessToken
        }
        resData = self.reqHttpData(url, 'get', data)
        return json.loads(resData)

    def initMenu(self):
        #创建菜单
        REDIRECT_URI='http://yituijian.com/wenjiebang'
        resumeUrl='https://open.weixin.qq.com/connect/oauth2/authorize?appid='+self.AppID+'&redirect_uri='+REDIRECT_URI+'&response_type=code&scope=snsapi_base&state=STATE#wechat_redirect'
        ## 点击跳转到简历首页的时候，去得到openid
        #resumeUrl='http://120.27.48.180:8085'
        buttonList = [
                {
                    "type":"view",
                    "name":"我要求职",
                    "url":resumeUrl
                },
                {
                    "type":"click",
                    "name":"我要招聘",
                    "key":"woyaozhaopin"
                },
                {
                    "type":"view",
                    "name":"百度一下",
                    "url":"http://www.baidu.com"
                },
            ]
        self.deleteMenu()
        self.createMenu(buttonList)

    def getOpenid(self,code):
        url = 'https://api.weixin.qq.com/sns/oauth2/access_token'
        data= {
            'grant_type': 'authorization_code',
            'appid': self.AppID,
            'secret': self.AppSecret,
            'code': code,
        }
        resData = self.reqHttpData(url, 'get', data)
        return json.loads(resData)       
        
wx = WechatApi()

wx.initMenu()

##print p.getCallbackIP()
##print p.getUserList()
##print p.getUserInfo('ojjAXw_I4EH8jb5onwO6yvIcHpM4')
##print p.getUserInfoBatchget(['ojjAXw_aVBT12Y6rZF4Xq5KNNIBQ','ojjAXwwJcQnzCP66F0zEpZRRo6Z8'])
##print p.sendCustomMsg('ojjAXw7TG-GLGzFphH6H66Z0S-ZI', 'test')

##print p.getMenu()

##xmlStr = '<xml><ToUserName><![CDATA[toUser]]></ToUserName> \
##            <FromUserName><![CDATA[fromUser]]></FromUserName>  \
##            <CreateTime>1348831860</CreateTime>     \
##            <MsgType><![CDATA[text]]></MsgType>     \
##            <Content><![CDATA[this is a test]]></Content>   \
##            <MsgId>1234567890123456</MsgId> </xml>'

##xmlStr = '''<xml>
##<ToUserName><![CDATA[toUser]]></ToUserName>
##<FromUserName><![CDATA[FromUser]]></FromUserName>
##<CreateTime>123456789</CreateTime>
##<MsgType><![CDATA[event]]></MsgType>
##<Event><![CDATA[subscribe]]></Event>
##</xml>'''
##print p.xmlToJson(xmlStr)

##p.jsonToXml({
##    "kf_account" : "test1@test",
##    "nickname" : u"客服1",
##    "password" : "pswmd5"
##})

