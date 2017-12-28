#-*- coding: utf-8 -*-
import markdown
from django.utils.html import strip_tags
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.six import python_2_unicode_compatible
# Create your models here.

@python_2_unicode_compatible
class Category(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Tag(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Post(models.Model):

    title = models.CharField(verbose_name='标题',max_length=70)
    body = models.TextField(verbose_name='内容')
    excerpt = models.CharField(verbose_name='文章摘要', max_length=200, blank=True)
    category = models.ForeignKey(Category, verbose_name='类型')
    tags = models.ManyToManyField(Tag, verbose_name='标签', blank=True)
    author = models.ForeignKey(User, verbose_name='作者')
    views = models.PositiveIntegerField(verbose_name='浏览量',default=0) #PositiveIntegerField 正整数
    created_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    modified_time = models.DateTimeField(verbose_name='最后修改时间', auto_now=True)
    
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_time']
    
    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])
    
    @property
    def comment_number(self):
        return self.comment_set.all().count

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    def save(self,*args,**kwargs):
        if not self.excerpt:
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            #strip_tags 删除html标记
            self.excerpt = strip_tags(md.convert(self.body))[:54]
        super(Post, self).save(*args,**kwargs)
