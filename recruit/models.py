#! -*- coding:utf-8 -*-
from django.db import models

# Create your models here.
class Recruit(models.Model):
	STATE_CHOICES = (
		(0, '未审核'),
		(1, '正常'),
		(2, '已下架'),
	)
	# 岗位名称
	position=models.CharField(max_length = 30)
	# 公司名称
	company=models.CharField(max_length = 30)
	# 学历要求
	degree=models.CharField(max_length = 30,blank=True)
	# 工作经验
	years=models.CharField(max_length = 30,blank=True)
	# 性别要求
	sex=models.CharField(max_length = 30,blank=True)
	# 工作地址
	address=models.CharField(max_length = 30,blank=True)
	# 薪水
	salary=models.CharField(max_length = 30,blank=True)
	# 职位描述
	description=models.CharField(max_length = 30)
	# 联系人
	contacts=models.CharField(max_length = 30)
	# 联系电话
	phone=models.CharField(max_length = 12)
	# 联系邮箱
	email=models.CharField(max_length = 30)
	# time
	create_time = models.DateTimeField(auto_now_add = True, blank = True)
	# 状态
	state=models.IntegerField(default = 0, choices = STATE_CHOICES)

class Connect(models.Model):
	STATE_CHOICES2 = (
		(0, '投递中'),
		(1, '投递成功'),
	)
	# 简历id
	resume_id=models.CharField(max_length = 30)
	# 招聘信息id
	recruit_id=models.CharField(max_length = 30)
	# 简历预览地址
	resume_address=models.CharField(max_length = 200,blank=True)
	# email
	email=models.CharField(max_length = 30,blank=True)
	# time
	create_time = models.DateTimeField(auto_now_add = True, blank = True)
	# 状态
	state=models.IntegerField(default = 0, choices = STATE_CHOICES2)

