from django.contrib import admin

from .models import Post, Category, LikePost, LikeComment, Comment, SeeLater

for i in [Post, Category, LikePost, LikeComment, Comment, SeeLater]:
    admin.site.register(i)