 # -*- coding: utf-8 -*- 
import urllib 
import urllib2 
import json

def get(url,data=None):
	if data:
		params = urllib.urlencode(data)
		url=url+'?'+params
	req = urllib2.Request(url)
	response= urllib2.urlopen(req)
	return json.loads(response.read())

def post(url, data): 
	req = urllib2.Request(url) 
	data = urllib.urlencode(data) 
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor()) 
	response = opener.open(req, data) 
	return json.loads(response.read())


class CMpConn(object):
	def __init__(self):
		self.AppID 		= 'wxea61534b1e615fd3'
		self.AppSecret 	= '0c7d2783e7dd86f7c2c9eff4d72b5ae1'
		self.accessToken = ''

	def mpGetAccessToken(self):#获取accessToken
		url='https://api.weixin.qq.com/cgi-bin/token'
		data= {'grant_type':'client_credential','appid':self.AppID,'secret':self.AppSecret}
		self.accessToken=get(url,data)['access_token']
		return self.accessToken

	def mpUserListGet(self):#获取openid
		url='https://api.weixin.qq.com/cgi-bin/user/get'
		data={'access_token':self.accessToken,'next_openid':''}
		return get(url,data)

	def mpUserInfoGet(self,openid):
		url='https://api.weixin.qq.com/cgi-bin/user/info'
		data={'access_token':self.accessToken,'openid':openid,'lang': 'zh_CN'}
		return get(url,data)
