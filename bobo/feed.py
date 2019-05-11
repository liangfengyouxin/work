from django.contrib.syndication.views import Feed
from .models import Bobo
from django.shortcuts import reverse

class BoboFeed(Feed):
    """
    进行网站包装成XML格式
    # RSS  可以把网站包装成XML格式
    # 可以通过RSS聚合工具订阅，该工具会回去RSS订阅更新的内容，
    # 不要每次进入博客查看更新

    """
    title = "微博博主"
    description = "最新更新的微博文章"
    link = '/'


    def items(self):
        return Bobo.objects.order_by('-create_time')[:5]

    def item_author(self, item):
        return item.author

    def item_content(self, item):
        return item.content

    def item_link(self, item):
        return reverse('bobo:detail', args=(item.id,))
