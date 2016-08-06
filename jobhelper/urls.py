from django.conf.urls import patterns, include, url
from django.contrib import admin
from jobhelper import view

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'jobhelper.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^resume/', include('resume.urls')),
    url(r'^recruit/', include('recruit.urls')),

    #url(r'^wechat/', view.wechat),

    url(r'^index$', view.index),

   	url(r'^wechatjob', view.wechatjob),

    url(r'^test$', view.test),

    url(r'^error$', view.error),


)
