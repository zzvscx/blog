from django.shortcuts import get_object_or_404,redirect,render
from blog.models import Post
from .models import Comment 
from .forms import CommentForm

# Create your views here.

def post_comment(request,post_pk):

    post = get_object_or_404(Post,pk=post_pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            print(comment)
            #redirect接受一个模型的实例时，会调用 get_absolute_url
            #然后重定向到返回的url
            return redirect(post)
        else:
            comment_list = post.comment_set.all()
            context = {
                'post': post,
                'form': form,
                'comment_list': comment_list
            }
        return render(request, 'blog/detail.html', locals())
    return redirect(post)
