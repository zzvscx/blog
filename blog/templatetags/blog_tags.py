from ..models import Post

def get_recent_posts(num=5):
    return Post.objects.all().order_by('-created_at')[:num]