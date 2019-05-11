from django import template
from ..models import Bobo
# django自定义模板和标签

#生成注册器
register = template.Library()


@register.simple_tag
# 获取浏览量最多的6篇博文
def get_recent_bobo_all(num=6):

    return Bobo.objects.all().order_by('-views')[:num]

# 根据微博发表月份进行排序和搜索，从而归档微博
@register.simple_tag
def archives():
    return Bobo.objects.dates('create_time','month',order='DESC')

#获取某个时间段中微博的总数
@register.simple_tag
def get_bobo_count_of_date(year,month):
    return Bobo.objects.filter(create_time__year=year,create_time__month=month).count()