from django.shortcuts import render
from django.db.models import Q,F
from . import models
import bobo

# Create your views here.

def shoucang_add(request,good_id):
    name = request.user.username
    # 得到用户收藏的微博
    _bo = bobo.models.Bobo.objects.get(pk=good_id)
    try:
        # 查询用户我的收藏中是否包含此微博
        shoucang = bobo.models.Shoucang.objects.get(Q(user=request.user) & Q(bo=_bo))
        shoucang.delete()

    except:
        #  如果不包含，创建收藏对象，添加的我的收藏
        shoucang = bobo.models.Shoucang(bo=_bo,user=request.user)
        shoucang.save()
    shoucang_list = bobo.models.Shoucang.objects.filter(user=request.user).order_by('-add_time')
    shoucang_num = len(shoucang_list)
    return render(request, 'shoucang/shoucang_info.html', locals())

def shoucang_info(request):
    name = request.user.username
    shoucang_all = bobo.models.Shoucang.objects.all()
    shoucang_list = bobo.models.Shoucang.objects.filter(user=request.user).order_by('-add_time')
    shoucang_num = len(shoucang_list)
    return render(request, 'shoucang/shoucang_info.html', locals())