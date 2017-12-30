#-*- coding:utf-8 -*-
import markdown
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from django.utils.text import slugify
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from markdown.extensions.toc import TocExtension

from .models import Post, Category, Tag
from comments.forms import CommentForm
# Create your views here.


class IndexView(ListView):

    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 5

class CategoryView(IndexView):
    def get_queryset(self):
        cate = get_object_or_404(Category,pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)

class ArchiveView(IndexView):
    
    def get_queryset(self):
        return super(ArchiveView, self).get_queryset().filter(created_time__year=self.kwargs.get('year'),
                                                created_time__month=self.kwargs.get('month'))

class TagView(IndexView):
    
    def get_queryset(self):
        tag = get_object_or_404(Tag,pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=tag)

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
        md = markdown.Markdown(extensions=[
                                'markdown.extensions.extra',
                                'markdown.extensions.codehilite',
                                TocExtension(slugify=slugify),
                            ])
        post.body = md.convert(post.body)
        post.toc = md.toc
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

def search(request):
    q = request.GET.get('q')
    error_msg = ''

    if not q:
        error_msg = '请输入关键词'
        return render (request, 'blog/index.html', locals())
    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request,'blog/index.html', locals())

