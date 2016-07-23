#! -*- coding:utf-8 -*-
from django.shortcuts import render
from resume.models import Resume,Education,Company
from resume import utils as comutils
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
import simplejson as json
# Create your views here.

@csrf_exempt
def fill_info(request):
	name = request.POST.get('name', None)
	sex = request.POST.get('sex', None)
	birth = request.POST.get('birth', None)
	startwork = request.POST.get('startwork', None)
	province = request.POST.get('province', None)
	city = request.POST.get('city', None)
	character = request.POST.get('character', None)
	phone = request.POST.get('phone', None)
	email = request.POST.get('email', None)
	try:
		r=Resume(name = name,
                sex = sex,
                birth = birth,
                start_work_date=startwork,
                province=province,
                city=city,
                character=character,
                phone=phone,
                email=email,
                nation='中国')
		r.save()
	except Exception, e:
		return comutils.baseresponse(e, 500)
	resume_id=Resume.objects.filter(phone=phone)[0].id
	return HttpResponse(json.dumps({'code':200,'resume_id':resume_id}))

@csrf_exempt
def modify_info(request):
	id=request.session.get('id',False)
	name = request.POST.get('name', None)
	sex = request.POST.get('sex', None)
	birth = request.POST.get('birth', None)
	startwork = request.POST.get('startwork', None)
	province = request.POST.get('province', None)
	city = request.POST.get('city', None)
	character = request.POST.get('character', None)
	phone = request.POST.get('phone', None)
	email = request.POST.get('email', None)
	try:
		Resume.objects.filter(id=id).update(name = name,
                sex = sex,
                birth = birth,
                start_work_date=startwork,
                province=province,
                city=city,
                character=character,
                phone=phone,
                email=email,
                nation='中国')
	except Exception, e:
		return comutils.baseresponse(e, 500)
	return HttpResponse(json.dumps({'code':200}))

@csrf_exempt
def fill_edu(request):
	resume_id = request.POST.get('resume_id', None)
	university = request.POST.get('university', None)
	intended_time = request.POST.get('intended_time', None)
	graduation_time = request.POST.get('graduation_time', None)
	major = request.POST.get('major', None)
	degree = request.POST.get('degree', None)
	resume=Resume.objects.filter(id=resume_id)[0]
	try:
		edu=Education(resume = resume,
                university = university,
                intended_time = intended_time,
                graduation_time=graduation_time,
                major=major,
                degree=degree)
		edu.save()
	except Exception, e:
		return comutils.baseresponse(e, 500)
	return HttpResponse(json.dumps({'code':200}))

@csrf_exempt
def modify_edu(request):
	edu_id = request.POST.get('edu_id', None)
	university = request.POST.get('university', None)
	intended_time = request.POST.get('intended_time', None)
	graduation_time = request.POST.get('graduation_time', None)
	major = request.POST.get('major', None)
	degree = request.POST.get('degree', None)
	try:
		Education.objects.filter(id=edu_id).update(university = university,
                intended_time = intended_time,
                graduation_time=graduation_time,
                major=major,
                degree=degree)
	except Exception, e:
		return comutils.baseresponse(e, 500)
	return HttpResponse(json.dumps({'code':200}))

@csrf_exempt
def delete_edu(request):
	edu_id = request.POST.get('edu_id', None)
	try:
		Education.objects.filter(id=edu_id).delete()
	except Exception, e:
		return comutils.baseresponse(e, 500)
	return HttpResponse(json.dumps({'code':200}))

@csrf_exempt
def fill_comp(request):
	resume_id = request.POST.get('resume_id', None)
	company = request.POST.get('company', None)
	entry_time = request.POST.get('entry_time', None)
	resign_time = request.POST.get('resign_time', None)
	position = request.POST.get('position', None)
	description = request.POST.get('description', None)
	resume=Resume.objects.filter(id=resume_id)[0]
	try:
		comp=Company(resume = resume,
                company = company,
                entry_time = entry_time,
                resign_time=resign_time,
                position=position,
                description=description)
		comp.save()
		Resume.objects.filter(id=resume_id).update(state=2)
	except Exception, e:
		return comutils.baseresponse(e, 500)
	return HttpResponse(json.dumps({'code':200}))

@csrf_exempt
def modify_comp(request):
	com_id = request.POST.get('com_id', None)
	company = request.POST.get('company', None)
	entry_time = request.POST.get('entry_time', None)
	resign_time = request.POST.get('resign_time', None)
	position = request.POST.get('position', None)
	description = request.POST.get('description', None)
	try:
		Company.objects.filter(id=com_id).update(company = company,
                entry_time = entry_time,
                resign_time=resign_time,
                position=position,
                description=description)
	except Exception, e:
		return comutils.baseresponse(e, 500)
	return HttpResponse(json.dumps({'code':200}))

@csrf_exempt
def delete_com(request):
	com_id = request.POST.get('com_id', None)
	try:
		Company.objects.filter(id=com_id).delete()
	except Exception, e:
		return comutils.baseresponse(e, 500)
	return HttpResponse(json.dumps({'code':200}))

#预览页面
def preview(request):
	id=request.session.get('id',False)
	r=Resume.objects.filter(id=id)[0]
	sex_choice={0:'保密',1:'男',2:'女'}
	info={'name':r.name,'phone':r.phone,'province':r.province,'city':r.city,'email':r.email,'sex':sex_choice[r.sex],'birth':r.birth,'startwork':r.start_work_date,'character':r.character,'avatar':r.avatar}
	edus=Education.objects.filter(resume=r)
	edu_info={}
	i=0
	for e in edus:
		edu_info[i]={'university':e.university,'intended_time':e.intended_time,'graduation_time':e.graduation_time,'major':e.major,'degree':e.degree}
		i=i+1
	coms=Company.objects.filter(resume=r)
	com_info={}
	i=0
	for c in coms:
		com_info[i]={'company':c.company,'entry_time':c.entry_time,'resign_time':c.resign_time,'position':c.position,'description':c.description}
		i=i+1
	return render_to_response('resume_preview.html',{'info':info,'edu_info':edu_info,'com_info':com_info})

#对外公开的预览页面
import base64
def preview_all(request,salt):
	decoded = base64.b64decode(salt)
	id=decoded.split('-')[0]
	r=Resume.objects.filter(id=id)[0]
	sex_choice={0:'保密',1:'男',2:'女'}
	info={'name':r.name,'phone':r.phone,'province':r.province,'city':r.city,'email':r.email,'sex':sex_choice[r.sex],'birth':r.birth,'startwork':r.start_work_date,'character':r.character,'avatar':r.avatar}
	edus=Education.objects.filter(resume=r)
	edu_info={}
	i=0
	for e in edus:
		edu_info[i]={'university':e.university,'intended_time':e.intended_time,'graduation_time':e.graduation_time,'major':e.major,'degree':e.degree}
		i=i+1
	coms=Company.objects.filter(resume=r)
	com_info={}
	i=0
	for c in coms:
		com_info[i]={'company':c.company,'entry_time':c.entry_time,'resign_time':c.resign_time,'position':c.position,'description':c.description}
		i=i+1
	return render_to_response('resume_preview.html',{'info':info,'edu_info':edu_info,'com_info':com_info})

#简历新建页
def fill(request):
	id=request.session.get('id',False)
	resume=Resume.objects.filter(id=id)[0]
	avatar=resume.avatar
	return render_to_response('resume_fill.html',{'id':id,'avatar':avatar})

#简历nav页
def nav(request):
	id=request.session.get('id',False)
	resume=Resume.objects.filter(id=id)[0]	
	state=resume.state
	province=resume.province
	city=resume.city
	avatar=resume.avatar
	name=resume.name
	edus_blank=1
	coms_blank=1
	state=1
	if state==0:
		return render_to_response('resume_blank.html')
	else:
		if state==1:
			edus=Education.objects.filter(resume=resume)
			coms=Company.objects.filter(resume=resume)
			if(len(edus)>0):
				edus_blank=0
			if(len(coms)>0):
				coms_blank=0
		return render_to_response('resume_nav.html',{'state':state,'id':id,'province':province,'city':city,'avatar':avatar,'name':name,'edus_blank':edus_blank,'coms_blank':coms_blank})
#简历info_list页
def info_list(request):
	id=request.session.get('id',False)
	r=Resume.objects.filter(id=id)[0]
	sex_choice={0:'保密',1:'男',2:'女'}
	info={'name':r.name,'phone':r.phone,'province':r.province,'city':r.city,'email':r.email,'sex':sex_choice[r.sex],'birth':r.birth,'startwork':r.start_work_date,'character':r.character,'avatar':r.avatar}
	print info
	return render_to_response('resume_info_list.html',{'info':info})


#简历edu_list页
def edu_list(request):
	id=request.session.get('id',False)
	resume=Resume.objects.filter(id=id)[0]	
	edus=Education.objects.filter(resume=resume)
	edu_info={}
	i=0
	for e in edus:
		edu_info[i]={'id':e.id,'university':e.university,'intended_time':e.intended_time,'graduation_time':e.graduation_time,'major':e.major,'degree':e.degree}
		i=i+1
	print edu_info
	return render_to_response('resume_edu_list.html',{'info':edu_info})

#简历edu_list页
def com_list(request):
	id=request.session.get('id',False)
	resume=Resume.objects.filter(id=id)[0]	
	coms=Company.objects.filter(resume=resume)
	com_info={}
	i=0
	for c in coms:
		com_info[i]={'id':c.id,'company':c.company,'entry_time':c.entry_time,'resign_time':c.resign_time,'position':c.position,'description':c.description}
		i=i+1
	return render_to_response('resume_com_list.html',{'info':com_info})

#展示和修改页
def modify(request,section,item_id):
	id=request.session.get('id',False)
	section=int(section)
	info={}
	if section==1:
		r=Resume.objects.filter(id=id)[0]
		sex_choice={0:'保密',1:'男',2:'女'}
		info={'name':r.name,'phone':r.phone,'province':r.province,'city':r.city,'email':r.email,'sex':sex_choice[r.sex],'birth':r.birth,'startwork':r.start_work_date,'character':r.character,'avatar':r.avatar}
	if section==2:
		e=Education.objects.filter(id=item_id)[0]
		info={'university':e.university,'intended_time':e.intended_time,'graduation_time':e.graduation_time,'major':e.major,'degree':e.degree}
	if section==3:
		c=Company.objects.filter(id=item_id)[0]
		info={'company':c.company,'entry_time':c.entry_time,'resign_time':c.resign_time,'position':c.position,'description':c.description}
	return render_to_response('resume_modify.html',{'section':section,'info':info})

