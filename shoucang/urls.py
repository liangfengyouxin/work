from django.conf.urls import url,include
from . import views


app_name = 'shoucang'
urlpatterns = [
    url(r'(?P<good_id>\d+)/shoucang_add/',views.shoucang_add,name='shoucang_add'),
    url(r'^shoucang_info/$', views.shoucang_info, name='shoucang_info'),



]