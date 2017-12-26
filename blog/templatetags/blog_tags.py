from django import template
from ..models import Post, Category

register = template.Library()

#获取最新的文章
@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.all().order_by('-created_time')[:num]

#将文章按月份归档
@register.simple_tag
def archives():
    return Post.objects.dates('created_time', 'month', order='DESC')

#类别
@register.simple_tag
def get_categories():
    return Category.objects.all()
