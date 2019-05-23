from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
# 微博文章模型
class Bobo(models.Model):
    # 字符串类型，微博文章模型中内容的长度和中文名
    content = models.CharField(max_length=140, verbose_name='微博内容')
    # 用户模型创建直接使用django内置模块。auth认证框架下的User
    author = models.ForeignKey(User, verbose_name='微博博主', on_delete=models.CASCADE)
    # 图片类型，微博文章模型中图片保存位置、图片保存可以为空和中文名
    # django对图片字段的处理：不会把图片本身的二进制数据保存到数据库，而是在数据库内保存指向图片路径，图片本身保存在指定目录下
    # 图片保存在weibo_image中，允许不配图。null=True表示在数据库内可以为空，blank=True表示在django后台界面admin中进行创建可为空。
    # 原则上null为空时,blank也为空，否则数据保存失败。
    img = models.ImageField(upload_to='bobo_image', null=True, blank=True, verbose_name='微博图片')
    # 正整数类型，浏览次数，默认值为0
    views = models.PositiveIntegerField(default=0, verbose_name='浏览次数')
    # 自动保存一条微博在创建时的时间和日期
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')

    # 在后台界面打印出微博内容，不加则打印出对象
    def __str__(self):
        return self.content

        # 自动生成每篇博客的微博详情url链接地址
    def get_absolute_url(self):
        return reverse('bobo:detail', args=(self.id,))

    # 增加浏览量
    def increase_views(self):
        self.views += 1
        # 为了减少不必要的工作，只保存views字段
        self.save(update_fields=['views'])

    # 定义类Meta，用于设置元信息
    class Meta():
        # 排序,默认为创建时间的反序，哪篇微博最新，最先展示
        ordering = ['-create_time']
        verbose_name = '微博内容'
        verbose_name_plural = '微博内容'



class Hotpic(models.Model):
    name = models.CharField(max_length=20)
    pic = models.ImageField(upload_to='lunbotu_image',null=True,blank=True,verbose_name='轮播图片')
    index = models.SmallIntegerField(unique=True)

    def __str__(self):
        return self.name

class Shoucang(models.Model):
    id = models.AutoField(primary_key=True)
    bo = models.ForeignKey('Bobo',on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    def __str__(self):
        return self.bo


