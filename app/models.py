from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator

from .utils import crop_img

User = get_user_model()

class Category(models.Model):
    title = models.CharField(max_length=100, unique=True, null=False)

    def save(self, force_insert=None, force_update=None, using=None, update_fields=None):
        self.title = self.title.lower().replace(" ", '-')
        return super().save(force_insert, force_update, using, update_fields)

class Post(models.Model):
    user = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='videos', on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='images', default='/download.jpeg')
    video = models.FileField(upload_to='videos', validators=[FileExtensionValidator(allowed_extensions=['mp4'])])
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(blank=True, null=True, default=0)

    def save(self):
        obj = super().save()
        crop_img(self.image.path)
        return obj

class Comment(models.Model):
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', related_name='sub_comments', on_delete=models.CASCADE, blank=True, null=True)

class LikePost(models.Model):
    user = models.ForeignKey(User, related_name='post_likes', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)

class LikeComment(models.Model):
    user = models.ForeignKey(User, related_name='comment_likes', on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, related_name='likes', on_delete=models.CASCADE)

class SeeLater(models.Model):
    user = models.ForeignKey(User, related_name='see_later', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='see_later', on_delete=models.CASCADE)
    seen = models.BooleanField(default=False)