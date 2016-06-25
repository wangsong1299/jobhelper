from django.contrib import admin

# Register your models here.
from recruit import models

class RecruitAdmin(admin.ModelAdmin):
    list_display = ('id', 'company')

class ConnectAdmin(admin.ModelAdmin):
    list_display = ('id', 'resume_id','recruit_id','state')

admin.site.register(models.Recruit, RecruitAdmin)
admin.site.register(models.Connect, ConnectAdmin)
