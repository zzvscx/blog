#-*- coding:utf-8 -*-
import markdown
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import Post
# Create your views here.

def index(request):
    post_list = Post.objects.all().order_by('-created_time')
    return render(request, 'blog/index.html', locals())

def detail(request, pk):
    post = get_object_or_404(Post,pk=pk)
    post.body = markdown.markdown(post.body,
                            extensions=[
                                'markdown.extensions.extra',
                                'markdown.extensions.codehilite',
                                'markdown.extensions.toc',
                            ])
    return render(request,'blog/detail.html', locals())




