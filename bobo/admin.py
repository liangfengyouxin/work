from django.contrib import admin
from . import models
# Register your models here.

# 自定义微博文章模型
class BoboAdmin(admin.ModelAdmin):
    list_display = ['content','author','img','views','create_time']


# 将微博文章模型注册
admin.site.register(models.Bobo,BoboAdmin)
# 将轮播图模型注册
admin.site.register(models.Hotpic)