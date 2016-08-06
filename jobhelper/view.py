# coding: utf-8
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
import simplejson as json
import datetime, time
import sys
import wechatApi
from resume.models import Resume,Education,Company

reload(sys)
sys.setdefaultencoding('utf8')

def index(request):
    path=request.get_full_path()
    path='?code=111&state=222'#test
    params=path.split('?')
    if(len(params)>1):
        param=params[1].split('&')
        for p in param:
            key=p.split('=')[0]
            if key=='code':
                code=p.split('=')[1]
        #openid=wechatApi.wx.getOpenid(code)['openid']
        openid='obqbYwPAb-4ATQ5ht2yxh5wpDjRE'#test
        resume=Resume.objects.filter(openid=openid)[0]
        id=resume.id
        province=resume.province
        city=resume.city
        avatar=resume.avatar
        name=resume.name
        request.session['id'] = id
        return render_to_response('home.html',{'province':province,'city':city,'avatar':avatar,'name':name})
    else:
        return HttpResponseRedirect("/error")

from lxml import etree
from django.utils.encoding import smart_str
@csrf_exempt
def wechatjob(request):
    try:
        if request.method == 'GET':
            timestamp = request.REQUEST.get('timestamp', '')
            nonce = request.REQUEST.get('nonce', '')
            echostr = request.REQUEST.get('echostr', '')
            signature = request.REQUEST.get('signature', '')  
            signature_my = wechatApi.wx.checkSignature(timestamp, nonce)
            print signature_my,signature,echostr,timestamp
            if signature==signature_my:
                return HttpResponse(echostr)
            else:
                return HttpResponse('FAILED')   
        elif request.method == 'POST':
            xml_str = smart_str(request.body)
            request_xml = xml_str
            # request_xml = etree.fromstring(xml_str)
            request_json = wechatApi.wx.xmlToJson(request_xml)
            print request_json

            msgType = request_json['xml']['MsgType']
            if 'Event' in request_json['xml']:
                event = request_json['xml']['Event']
            if 'EventKey' in request_json['xml']:
                eventKey = request_json['xml']['EventKey']
            fromUserName = request_json['xml']['FromUserName']
            toUserName = request_json['xml']['ToUserName']
            content = request_json['xml']['Content']

            response_json = {
                'ToUserName': fromUserName,
                'FromUserName': toUserName,
                'CreateTime': int(time.time()),
                'MsgType': 'text',
                'Content': content
            }

            response_xml = wechatApi.wx.jsonToReturnXml(response_json)
            print response_xml
            # if msgType=='event':
            #     if event=='VIEW':
            #         info=wechatApi.wx.getUserInfo(openid)
            #         user=Resume.objects.filter(openid=openid)
            #         if len(user)==0:
            #             province=info['province']
            #             city=info['city']
            #             nickname=info['nickname']
            #             headimgurl=info['headimgurl']
            #             nation=info['country']
            #             r=Resume(name = nickname,
            #                     openid = openid,
            #                     province=province,
            #                     city=city,
            #                     avatar=headimgurl,
            #                     nation=nation)
            #             r.save()
            #         else:
            #             print 'user already exist'
            return HttpResponse(response_xml)
    except Exception, e:
        print e
    

def test(request):
    return render_to_response('test.html')

def error(request):
    return render_to_response('test.html')

