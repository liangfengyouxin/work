from django.conf.urls import url,include
from . import views


app_name = 'guanzhu'
urlpatterns = [
    url(r'(?P<guan_id>\d+)/shoucang_add/',views.guanzhu_add,name='guanzhu_add'),




]