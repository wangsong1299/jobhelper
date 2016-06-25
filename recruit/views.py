#! -*- coding:utf-8 -*-
from django.shortcuts import render
from recruit.models import Recruit,Connect
from resume import utils as comutils
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
import simplejson as json

#预览页面
def index(request):
	recruits=Recruit.objects.filter(state=0)
	recruit_info={}
	i=0
	for r in recruits:
		recruit_info[i]={'company':r.company,'description':r.description,'id':r.id}
		i=i+1
	return render_to_response('recruit.html',{'recruit_info':recruit_info})
#首页

#我的投递
def myshow(request,id):
	connects=Connect.objects.filter(resume_id=id)
	myshow_info={}
	i=0
	for c in connects:
		recruit_id=c.recruit_id
		r=Recruit.objects.filter(id=recruit_id)[0]
		myshow_info[i]={'company':r.company,'description':r.description,'id':recruit_id}
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
			resume_address = 'http://127.0.0.1:8000/resume/preview_all/'+str(salt)
			email=Recruit.objects.filter(id=recruit_id)[0].email
			conn=Connect(resume_id = resume_id,recruit_id=recruit_id,resume_address=resume_address,email=email)
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
