from django.conf.urls import url,include
from . import views
from .feed import BoboFeed
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap




# 给weibo应用添加命令空间,app所有路由由此开头
app_name = 'bobo'
urlpatterns = [
    #http://127.0.0.1/weibo/    #建立/index和视图index之间的关系
    url(r'^$',views.index,name='index'),
    #显示微博文章详情,(\d+)为组,django在调用视图函数时,组的内容为参数,可传入到对应的视图函数中去
    url(r'^detail/(\d+)/$',views.detail,name='detail'),
    url(r'^search/$',views.search,name='search'),
    url(r'^archives/(?P<year>[0-9]+)/(?P<month>[0-9]+)/$', views.archives, name='archives'),
    url(r'^rss/$',BoboFeed(),name='rss'),
    url(r'^reply/(?P<comment_id>\d+)/$',views.reply,name='reply'),
    url(r'^articlepublish/$', views.articlepublish, name='articlepublish'),
    url(r'^article_list/$', views.article_list, name='article_list'),
    url(r'^detele/(\d+)/$', views.detele, name='detele'),
    url(r'^user_list/(\d+)/$', views.user_list, name='user_list'),

]