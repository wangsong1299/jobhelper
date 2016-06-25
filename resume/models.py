#! -*- coding:utf-8 -*-
from django.db import models

# Create your models here.
class Resume(models.Model):
	#default
	DEFAULT_AVATAR = 'headimage.png'
	UNKNOWN = 0
	MEAL = 1
	FEMEAL = 2
	SEX_CHOICES = (
		(UNKNOWN, '保密'),
		(MEAL, '男'),
		(FEMEAL, '女'),
	)

	STATE_CHOICES = (
		(0, '空白'),
		(1, '不完整'),
		(2, '完整,未审核'),
		(3, '已审核'),
	)

	#名字
	name=models.CharField(max_length = 30)
	openid=models.CharField(max_length = 60)
	#国家省份城市
	nation=models.CharField(max_length = 30)
	province=models.CharField(max_length = 30)
	city=models.CharField(max_length = 30)
		# 手机号码
	phone = models.CharField(max_length = 12, unique = True)
		# 头像
	avatar = models.CharField(max_length = 200, blank = True, default = DEFAULT_AVATAR)
	# 性别
	sex = models.IntegerField(default = UNKNOWN, choices = SEX_CHOICES)
	# 出生年月
	birth=models.CharField(max_length = 30)
	# 参加工作时间
	start_work_date=models.CharField(max_length = 30)
	# 性格描述
	character=models.CharField(max_length = 100)
	# 邮箱地址
	email=models.CharField(max_length = 30)
	# 简历状态
	state=models.IntegerField(default = 1, choices = STATE_CHOICES)

	def __unicode__(self):
		return unicode(self.id) + '_' + self.name


    ## 教育信息
class Education(models.Model):
	resume = models.ForeignKey('resume.Resume')
	# 学校名称
	university=models.CharField(max_length = 30)
	# 入学时间
	intended_time=models.CharField(max_length = 30)
	# 毕业时间
	graduation_time=models.CharField(max_length = 30)
	# 专业名称
	major=models.CharField(max_length = 30)
	# 学历/学位
	degree=models.CharField(max_length = 30)
	# 产生时间
	create_time = models.DateTimeField(auto_now_add = True, blank = True)

    ## 工作信息
class Company(models.Model):
	resume = models.ForeignKey('resume.Resume')
	# 公司名称
	company=models.CharField(max_length = 30)
	# 入职时间
	entry_time=models.CharField(max_length = 30)
	# 离职时间
	resign_time=models.CharField(max_length = 30)
	# 岗位名称
	position=models.CharField(max_length = 30)
	# 工作描述
	description=models.CharField(max_length = 200)
	# 产生时间
	create_time = models.DateTimeField(auto_now_add = True, blank = True)
