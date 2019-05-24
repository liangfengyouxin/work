from django.shortcuts import render,redirect,get_object_or_404,reverse
from . import models
from django.db.models import Q
from django_comments.models import Comment
from collections import Counter
from django.http import HttpResponse,HttpResponseRedirect,HttpRequest
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django_comments.models import Comment
from django_comments import models as comment_models
from django.db.models import Q,F


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




def pagination_data(paginator, page):
    """
    用于自定义展示分页页码的方法
    :param paginator: Paginator类的对象
    :param page: 当前请求的页码
    :return: 一个包含所有页码和符号的字典
    """
    if paginator.num_pages == 1:
        # 如果无法分页，也就是只有1页不到的内容，则无需显示分页导航条，不用任何分页导航条的数据，因此返回一个空的字典
        return {}
    # 当前页左边连续的页码号，初始值为空
    left = []

    # 当前页右边连续的页码号，初始值为空
    right = []

    # 标示第 1 页页码后是否需要显示省略号
    left_has_more = False

    # 标示最后一页页码前是否需要显示省略号
    right_has_more = False

    # 标示是否需要显示第 1 页的页码号。
    # 因为如果当前页左边的连续页码号中已经含有第 1 页的页码号，此时就无需再显示第 1 页的页码号，
    # 其它情况下第一页的页码是始终需要显示的。
    # 初始值为 False
    first = False

    # 标示是否需要显示最后一页的页码号。
    # 需要此指示变量的理由和上面相同。
    last = False

    # 获得用户当前请求的页码号
    try:
        page_number = int(page)
    except ValueError:
        page_number = 1
    except:
        page_number = 1

    # 获得分页后的总页数
    total_pages = paginator.num_pages

    # 获得整个分页页码列表，比如分了四页，那么就是 [1, 2, 3, 4]
    page_range = paginator.page_range

    if page_number == 1:
        # 如果用户请求的是第一页的数据，那么当前页左边的不需要数据，因此 left=[]（已默认为空）。
        # 此时只要获取当前页右边的连续页码号，
        # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 right = [2, 3]。
        # 注意这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
        right = page_range[page_number:page_number + 4]

        # 如果最右边的页码号比最后一页的页码号减去 1 还要小，
        # 说明最右边的页码号和最后一页的页码号之间还有其它页码，因此需要显示省略号，通过 right_has_more 来指示。
        if right[-1] < total_pages - 1:
            right_has_more = True

        # 如果最右边的页码号比最后一页的页码号小，说明当前页右边的连续页码号中不包含最后一页的页码
        # 所以需要显示最后一页的页码号，通过 last 来指示
        if right[-1] < total_pages:
            last = True

    elif page_number == total_pages:
        # 如果用户请求的是最后一页的数据，那么当前页右边就不需要数据，因此 right=[]（已默认为空），
        # 此时只要获取当前页左边的连续页码号。
        # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 left = [2, 3]
        # 这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
        left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]

        # 如果最左边的页码号比第 2 页页码号还大，
        # 说明最左边的页码号和第 1 页的页码号之间还有其它页码，因此需要显示省略号，通过 left_has_more 来指示。
        if left[0] > 2:
            left_has_more = True

        # 如果最左边的页码号比第 1 页的页码号大，说明当前页左边的连续页码号中不包含第一页的页码，
        # 所以需要显示第一页的页码号，通过 first 来指示
        if left[0] > 1:
            first = True
    else:
        # 用户请求的既不是最后一页，也不是第 1 页，则需要获取当前页左右两边的连续页码号，
        # 这里只获取了当前页码前后连续两个页码，你可以更改这个数字以获取更多页码。
        left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
        right = page_range[page_number:page_number + 2]

        # 是否需要显示最后一页和最后一页前的省略号
        if right[-1] < total_pages - 1:
            right_has_more = True
        if right[-1] < total_pages:
            last = True

        # 是否需要显示第 1 页和第 1 页后的省略号
        if left[0] > 2:
            left_has_more = True
        if left[0] > 1:
            first = True

    data = {
        'left': left,
        'right': right,
        'left_has_more': left_has_more,
        'right_has_more': right_has_more,
        'first': first,
        'last': last,
    }
    return data




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
    page_data = pagination_data(paginator,page)
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

    comment_list = list()
    def get_comment_list(comments):
        for comment in comments:
            comment_list.append(comment)
            children = comment.child_comment.all()
            if len(children) > 0:
                get_comment_list(children)

    top_comments = Comment.objects.filter(object_pk=id,parent_comment=None,
                                          content_type__app_label='bobo').order_by('-submit_date')
    get_comment_list(top_comments)

    return render(request, 'bobo/detail.html', locals())

def search(request):
    name = request.user.username
    # 在搜索的视图函数中获取关键字，没有关键字则获取为None
    keyword = request.GET.get('keyword',None)

    if not keyword:
        error_msg = '请输入关键字'
        return render(request,'bobo/index.html',locals())
    # 过滤函数中使用Q对象查询微博文章中是否包含关键字
    bobo_search = models.Bobo.objects.filter(Q(content__icontains=keyword))
    # 从request请求中的get方法中获取page的值，如果有则page的值为page，如果没有，page的值为1
    page = request.GET.get('page', 1)
    # 当前页需要展示的微博文章，请求页码，每页显示微博文章的数量
    bobo_list, paginator = make_paginator(bobo_search, page)
    page_data = pagination_data(paginator, page)
    return render(request, 'bobo/index.html', locals())


def archives(request,year,month):
    name = request.user.username
    bobo_archives = models.Bobo.objects.filter(create_time__year=year,create_time__month=month)
    # 从request请求中的get方法中获取page的值，如果有则page的值为page，如果没有，page的值为1
    page = request.GET.get('page', 1)
    # 当前页需要展示的微博文章，请求页码，每页显示微博文章的数量
    bobo_list, paginator = make_paginator(bobo_archives, page)
    page_data = pagination_data(paginator, page)
    return render(request, 'bobo/index.html', locals())


def reply(request,comment_id):
    name = request.user.username
    parent_comment = get_object_or_404(comment_models.Comment,id=comment_id)
    return render(request,'bobo/reply.html',locals())

def articlepublish(request):
    name = request.user.username
    if request.method == 'GET':
        return render(request, 'bobo/article_publish.html', locals())
    elif request.method == 'POST':
        content = request.POST['content']
        author_id = request.user.id
        img = request.FILES['tupian']
        article = models.Bobo(content=content,author_id=author_id,img=img)
        article.save()
        return redirect(reverse('bobo:index'))

def article_list(request):
    name = request.user.username
    id = request.user.id
    bobo_list = models.Bobo.objects.filter(author_id=id)
    bobo_num = len(bobo_list)
    return render(request,'bobo/article_list.html',locals())

def detele(request,bobo_id):
    name = request.user.username
    bobo = models.Bobo.objects.get(pk=bobo_id)
    bobo.delete()
    id = request.user.id
    bobo_list = models.Bobo.objects.filter(author_id=id)
    return render(request, 'bobo/article_list.html', locals())


def user_list(request,user_id):
    name = request.user.username
    user_list = models.User.objects.filter(id=user_id)
    for user in user_list:
        print(user.username)
        user_list = models.Bobo.objects.filter(author_id=user.id)
        bobo_num = len(user_list)

        return render(request,'bobo/user_list.html',locals())






