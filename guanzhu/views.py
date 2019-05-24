from django.shortcuts import render
from django.db.models import Q,F
from . import models
import bobo

# Create your views here.
def guanzhu_add(request,guan_id):
    name = request.user.username
    # 得到用户关注的博主
    bozhu = bobo.models.User.objects.get(pk=guan_id)
    try:
        # 查询用户我的关注中是否包含此博主
        guanzhu = bobo.models.Guanzhu.objects.get(Q(guanzhu_user=bozhu))
        guanzhu.delete()
        
    except:
        #  如果不包含，创建关注对象，添加的我的关注
        guanzhu = bobo.models.Guanzhu(guanzhu_user=bozhu)
        guanzhu.save()


    guanzhu_list = bobo.models.Guanzhu.objects.all().order_by('-addguan_time')
    for guanzhu in guanzhu_list:
        print(guanzhu.guanzhu_user_id)
        bozhuming = bobo.models.User.objects.get(pk=guanzhu.guanzhu_user_id)
        print(bozhuming.username)
    guanzhu_num = len(guanzhu_list)
    return render(request, 'guanzhu/guanzhu_info.html', locals())

