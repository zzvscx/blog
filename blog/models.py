#-*- coding: utf-8 -*-
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
    created_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    modified_time = models.DateTimeField(verbose_name='最后修改时间', auto_now=True)
    
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_time']


    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})