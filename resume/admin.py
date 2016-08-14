from django.contrib import admin

# Register your models here.
from resume import models

# Register your models here.
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','phone','sex','state')

class EducationAdmin(admin.ModelAdmin):
    list_display = ('id', 'resume','university','major','degree')

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'resume','company','position')

class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'productImg')

admin.site.register(models.Resume, ResumeAdmin)
admin.site.register(models.Education, EducationAdmin)
admin.site.register(models.Company, CompanyAdmin)
admin.site.register(models.Image, ImageAdmin)

