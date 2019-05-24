"""work URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path,re_path
from django.conf.urls import url,include
from django.conf import settings
from django.conf.urls.static import static
from bobo.feed import BoboFeed

urlpatterns = [
    path('admin/', admin.site.urls),
    #每个以 开头的路由，都会转发到weibo下的urls中
    url(r'^',include('bobo.urls',namespace='bobo')),
    re_path(r'^accounts/', include('allauth.urls')),
    url(r'^latest/feed/$',BoboFeed()),
    url(r'^comments/', include('django_comments.urls')),
    url(r'shoucang/',include('shoucang.urls',namespace='shoucang')),
    # url(r'guanzhu/',include('guanzhu.urls',namespace='guanzhu')),

]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
# 配置用户发的图片存储地址,不写会微博图片和轮播图片显示加载失败
