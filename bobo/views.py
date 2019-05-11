from django.shortcuts import render,redirect,get_object_or_404
from . import models
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger


# Create your views here.
# 微博分页,接收参数：对象列表,第几页，每页显示博文数量
def make_paginator(objects,page,num=6):
    # 利用分页器生成对象,objects为所有的微博文章
    paginator = Paginator(objects,num)
    try:
        object_list = paginator.page(page)
    except PageNotAnInteger:
        object_list = paginator.page(1)
    except EmptyPage:
        object_list = paginator.page(paginator.num_pages)

    return object_list,paginator


def index(request):

    name=request.user.username
    # 轮播图
    hotpic = models.Hotpic.objects.all().order_by('index')
    # 获取所有微博
    bobo_all = models.Bobo.objects.all()
    # 从request请求中的get方法中获取page的值，如果有则page的值为page，如果没有，page的值为1
    page = request.GET.get('page', 1)
    # 当前页需要展示的微博文章，请求页码，每页显示微博文章的数量
    bobo_list, paginator = make_paginator(bobo_all, page)
    # 1.加载模板文件，得到模板对象
    # 2.定义模板上下文：给模板文件传递数据
    # 3.使用变量参数渲染模板: 产生标准的html内容
    # 返回给浏览器
    return render(request, 'bobo/index.html', locals())


def detail(request,id):
    name = request.user.username
    bobo = get_object_or_404(models.Bobo, id=id)
    # 每点击一次微博详情页面，那个微博浏览量就会加1
    bobo.increase_views()

    return render(request, 'bobo/detail.html', locals())
