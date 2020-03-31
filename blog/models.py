from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

# Create your models here.


class PostCategory(models.Model):
    cat_title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(blank=True)
    cat_desc = models.TextField()

    class Meta:
        verbose_name = 'Post Category'
        verbose_name_plural = 'Post Categories'

    def __str__(self):
        return self.cat_title


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    thumb = models.URLField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    featured = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    category = models.ForeignKey(
        PostCategory, null=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.title


class Like(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(
        Post, related_name='likes', on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(
        Post, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    body = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)


@receiver(pre_save, sender=Post)
def pre_save_slug(sender, **kwargs):
    slug = slugify(kwargs['instance'].title)
    kwargs['instance'].slug = slug
