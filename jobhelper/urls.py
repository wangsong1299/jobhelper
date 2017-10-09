from django.conf.urls import include, url
from django.contrib import admin
from jobhelper import view

urlpatterns = [

    url(r'^admin/', include(admin.site.urls)),
    url(r'^resume/', include('resume.urls')),
    url(r'^recruit/', include('recruit.urls')),

    #url(r'^wechat/', view.wechat),
    url(r'^$', view.redirect),
    url(r'^index$', view.index),

   	url(r'^wechatjob', view.wechatjob),

    url(r'^test$', view.test),

    url(r'^error$', view.error),

    url(r'^upload/$',view.upload),

]
