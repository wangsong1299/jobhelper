#! -*- coding:utf-8 -*-
from django.shortcuts import render
from recruit.models import Recruit,Connect
from resume import utils as comutils
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
import simplejson as json
import datetime

#招聘信息页面
def index(request):
	id=request.session.get('id',False)
	recruits=Recruit.objects.filter(state=1).order_by('-id')
	recruit_info={}
	i=0
	now = datetime.datetime.now()
	nowtime=time.mktime(now.timetuple())
	for r in recruits:
		create_time=time.mktime(r.create_time.timetuple())
		timediff=nowtime-create_time
		timediffday=str(int(timediff/(60*60*24)))
		timediffHour=str(int(timediff/(60*60)))
		timediffSec=str(int(timediff/(60)))
		if(timediffday>0):
			timeGo=timediffday+'天'
		elif(timediffHour>0):
			timeGo=timediffHour+'小时'
		else:
			timeGo=timediffSec+'分'
		recruit_info[i]={'position':r.position,'company':r.company,'degree':r.degree,'years':r.years,'sex':r.sex,'address':r.address,'salary':r.salary,'description':r.description,'id':r.id,'resume_id':id,'timeGo':timeGo}
		i=i+1
	return render_to_response('recruit.html',{'recruit_info':recruit_info})
#首页

#我的投递
def myshow(request,id):
	id=request.session.get('id',False)
	connects=Connect.objects.filter(resume_id=id).order_by('-id')
	myshow_info={}
	i=0
	now = datetime.datetime.now()
	nowtime=time.mktime(now.timetuple())
	for c in connects:
		create_time=time.mktime(c.create_time.timetuple())
		timediff=nowtime-create_time
		timediffday=str(int(timediff/(60*60*24)))
		timediffHour=str(int(timediff/(60*60)))
		timediffSec=str(int(timediff/(60)))
		if(timediffday>0):
			timeGo=timediffday+'天'
		elif(timediffHour>0):
			timeGo=timediffHour+'小时'
		else:
			timeGo=timediffSec+'分'
		recruit_id=c.recruit_id
		r=Recruit.objects.filter(id=recruit_id)[0]
		myshow_info[i]={'position':r.position,'company':r.company,'years':r.years,'degree':r.degree,'sex':r.sex,'salary':r.salary,'id':recruit_id,'state':c.state,'resume_id':id,'timeGo':timeGo}
		i=i+1
	return render_to_response('myrecruit.html',{'myshow_info':myshow_info})


import base64
import time
#api
@csrf_exempt
def fill_connect(request):
	resume_id = request.POST.get('resume_id', None)
	recruit_id = request.POST.get('recruit_id', None)
	c=Connect.objects.filter(resume_id = resume_id).filter(recruit_id=recruit_id)
	if c:
		return HttpResponse(json.dumps({'code':201}))
	else:
		try:
			key=str(resume_id)+'-'+str(time.time())
			salt = base64.b64encode(key)
			resume_address = 'http://yituijian.com/resume/preview_all/'+str(salt)
			resume_address2 = 'http://yituijian.com/resume/preview_all2/'+str(salt)
			email=Recruit.objects.filter(id=recruit_id)[0].email
			conn=Connect(resume_id = resume_id,recruit_id=recruit_id,resume_address=resume_address,resume_address2=resume_address2,email=email)
			conn.save()
		except Exception, e:
			return comutils.baseresponse(e, 500)
		return HttpResponse(json.dumps({'code':200}))

@csrf_exempt
def delete_connect(request):
	resume_id = request.POST.get('resume_id', None)
	recruit_id = request.POST.get('recruit_id', None)
	try:
		Connect.objects.filter(resume_id = resume_id).filter(recruit_id=recruit_id).delete()
	except Exception, e:
		return comutils.baseresponse(e, 500)
	return HttpResponse(json.dumps({'code':200}))

