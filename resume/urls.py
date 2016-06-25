#! -*- coding:utf-8 -*-
from django.conf.urls import patterns, include, url
from resume import views
from resume import tests

urlpatterns = patterns('',
    # 首页
    #url(r'^home/$', views.home),
    
     url(r'^fill_info/$', views.fill_info),
     url(r'^fill_edu/$', views.fill_edu),
     url(r'^fill_comp/$', views.fill_comp),
     url(r'^modify_info/$', views.modify_info),
     url(r'^modify_edu/$', views.modify_edu),
     url(r'^modify_comp/$', views.modify_comp),

     #预览页
     url(r'^preview$', views.preview),
     url(r'^preview_all/(\w{1,100})/$', views.preview_all),
     #对外的预览页


     url(r'^nav/$', views.nav),
     #信息列表页
     url(r'^edu_list/$', views.edu_list),
     url(r'^com_list/$', views.com_list),
     #信息展示和修改页
     url(r'^modify/(\d{1,6})/(\d{1,6})/$', views.modify),
     url(r'^fill/$', views.fill),







)

