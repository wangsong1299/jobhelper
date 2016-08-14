# coding: utf-8
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
import simplejson as json
import datetime, time
import sys
import wechatApi
from resume.models import Resume,Education,Company
from HrStatus import rds # HrStatus
import pdb
from resume import utils as comutils
from recruit.models import Recruit,Connect

reload(sys)
sys.setdefaultencoding('utf8')

def index(request):
    path=request.get_full_path()
    #path='index?code=111&state='#test
    #print path
    params=path.split('?')
    if(len(params)>1):
        param=params[1].split('&')
        for p in param:
            key=p.split('=')[0]
            if key=='code':
                code=p.split('=')[1]
        #print code
        data = wechatApi.wx.getOpenid(code)
        if('openid' in data):
            openid=data['openid']
            user=Resume.objects.filter(openid=openid)
            if len(user)==0:
                info=wechatApi.wx.getUserInfo(openid)
                print info
                province=info['province']
                city=info['city']
                nickname=info['nickname']
                headimgurl=info['headimgurl']
                nation=info['country']
                r=Resume(name = nickname,
                        openid = openid,
                        province=province,
                        city=city,
                        avatar=headimgurl,
                        nation=nation,
                        state=0)
                r.save()
            else:
                print 'user already exist'
            resume=Resume.objects.filter(openid=openid)[0]
        else:
            #request.session['id'] = 2#test
            id=request.session.get('id',False)
            resume=Resume.objects.filter(id=id)[0]
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
            #print signature_my,signature,echostr,timestamp
            if signature==signature_my:
                return HttpResponse(echostr)
            else:
                return HttpResponse('FAILED')   
        elif request.method == 'POST':
            xml_str = smart_str(request.body)
            request_xml = xml_str
            # request_xml = etree.fromstring(xml_str)
            request_json = wechatApi.wx.xmlToJson(request_xml)
            #print request_json
            msgType = request_json['xml']['MsgType']
            if 'Event' in request_json['xml']:
                event = request_json['xml']['Event']
            fromUserName = request_json['xml']['FromUserName']
            toUserName = request_json['xml']['ToUserName']
            if 'Content' in request_json['xml']:
                content = request_json['xml']['Content']
            else:
                content = ''

            #事件触发
            if 'EventKey' in request_json['xml']:
                eventKey = request_json['xml']['EventKey']
                #判断是否是点击『我要招聘』
                if(eventKey=='woyaozhaopin'):
                    tip = rds.setStatus(fromUserName, 'reset')
                    response_json = {
                        'ToUserName': fromUserName,
                        'FromUserName': toUserName,
                        'CreateTime': int(time.time()),
                        'MsgType': 'text',
                        'Content': tip 
                    }
                   #print tip
                else:
                    response_json = {
                        'ToUserName': fromUserName,
                        'FromUserName': toUserName,
                        'CreateTime': int(time.time()),
                        'MsgType': 'text',
                        'Content': '系统错误，请重新发送'
                    }          
            else:
                tip = rds.setStatus(fromUserName, content)
                #over表示接收完成，如没完成则执行下一步
                if(tip!='over'):
                    response_json = {
                        'ToUserName': fromUserName,
                        'FromUserName': toUserName,
                        'CreateTime': int(time.time()),
                        'MsgType': 'text',
                        'Content': tip 
                    }
                else:
                    info=rds.getInfo(fromUserName)
                    #print info
                    try:
                        r=Recruit(position = info['1'],company = info['2'],degree = info['3'],years=info['4'],address=info['5'],sex=info['6'],salary=info['7'],description=info['8'])
                        r.save()
                    except Exception, e:
                        return comutils.baseresponse(e, 500)
                    infotext="职位:"+info['1']+'_公司:'+info['2']+'_学历要求:'+info['3']+'_年限要求:'+info['4']+'_公司地址:'+info['5']+'_性别要求:'+info['6']+'_薪水范围:'+info['7']+'_工作描述:'+info['8']
                    response_json = {
                        'ToUserName': fromUserName,
                        'FromUserName': toUserName,
                        'CreateTime': int(time.time()),
                        'MsgType': 'text',
                        'Content': '您好，您已完成招聘信息的填写,管理员审核通过后可在招聘信息处呈现。信息如下:'+infotext
                    }                
            response_xml = wechatApi.wx.jsonToReturnXml(response_json)
            return HttpResponse(response_xml)
    except Exception, e:
        print e


def test(request):
    request.session['id'] = 2
    return render_to_response('test.html')

def error(request):
    return render_to_response('test.html')

def redirect(request):
    return HttpResponseRedirect("/index")

