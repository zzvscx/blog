#-*- coding:utf-8 -*-
import markdown
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Post, Category
from comments.forms import CommentForm
# Create your views here.


class IndexView(ListView):

    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

class CategoryView(IndexView):
    def get_queryset(self):
        cate = get_object_or_404(Category,pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)

class ArchivesView(IndexView):
    
    def get_queryset(self):
        print(self.kwargs.get('year'))
        print(self.kwargs.get('month'))
        return super(ArchivesView, self).get_queryset().filter(created_time__year=self.kwargs.get('year'),
                                                created_time__month=self.kwargs.get('month'))

class PostDetailView(DetailView):

    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        self.object.increase_views()
        return response

    def get_object(self, queryset=None):

        post = super(PostDetailView, self).get_object(queryset=None)
        post.body = markdown.markdown(post.body,
                            extensions=[
                                'markdown.extensions.extra',
                                'markdown.extensions.codehilite',
                                'markdown.extensions.toc',
                            ])
        return post

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'form': form,
            'comment_list': comment_list,
        })
        return context
