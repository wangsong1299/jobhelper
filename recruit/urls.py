#! -*- coding:utf-8 -*-
from django.conf.urls import include, url
from recruit import views
from recruit import tests

urlpatterns = [

    url(r'^$', views.index),
    url(r'^myshow/(\d{1,6})/$', views.myshow),


#api
    url(r'^fill_connect/$', views.fill_connect),
    url(r'^delete_connect/$', views.delete_connect),

]

