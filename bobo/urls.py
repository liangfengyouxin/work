from django.conf.urls import url,include
from . import views



# 给weibo应用添加命令空间,app所有路由由此开头
app_name = 'bobo'
urlpatterns = [
    #http://127.0.0.1/weibo/    #建立/index和视图index之间的关系
    url(r'^$',views.index,name='index'),
    #显示微博文章详情,(\d+)为组,django在调用视图函数时,组的内容为参数,可传入到对应的视图函数中去
    url(r'^detail/(\d+)/$',views.detail,name='detail'),

]