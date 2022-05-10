from django.urls import path

from .views import *
from .services import get_streaming_video

urlpatterns = [
    path('see/<int:pk>/', see, name='see'),
    path('videos/mine/', my_posts, name='my_videos'),
    path('video/create/', create_video_view, name='create_video'),
    path('video/update/<int:pk>/', update_video_view, name='update_video'),

    path('see_later/<int:pk>/', add_see_later, name='see_later'),
    path('see_later_list/', see_later_list, name='see_later_list'),

    path('likes/mine/', my_likes, name='liked'),
    path('like/post/<int:pk>/', toggle_like_post, name='like_post'),
    path('like/comment/<int:post_id>/<int:pk>/', toggle_like_comment, name='like_comment'),
    path('comment/create/<int:pk>/', add_comment, name='create_comment'),

    path('stream/<int:pk>/', get_streaming_video, name='stream'),
    
    path('', search_video, name='search'),
    path('<str:category>/', search_video, name='search_by_category'),
]
