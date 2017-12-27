from django.db import models
from django.utils.six import python_2_unicode_compatible
# Create your models here.

@python_2_unicode_compatible
class Comment(models.Model):
    name = models.CharField(verbose_name='用户名', max_length=100)
    email = models.EmailField(verbose_name='用户邮箱', max_length=100)
    url = models.URLField(verbose_name='用户主页', blank=True)
    text = models.TextField()
    created_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    post = models.ForeignKey('blog.Post')

    def __str__(self):
        return self.text[:20]

    class Meta:
        ordering = ['-created_time']

