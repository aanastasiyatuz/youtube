from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import RegisterView, SignInView, activate, profile, follow_create, see_follow

urlpatterns = [
    path('sign_up/', RegisterView.as_view(), name="register"),
    path('login/', SignInView.as_view(), name='login'),
    path('activate/<str:activation_code>/', activate, name='activate'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('profile/', profile, name='my_profile'),
    path('profile/<str:user>/', profile, name='profile'),

    path('follow/<str:user>/', follow_create, name='follow_create'),
    path('see_follow/<str:user>/', see_follow, name='see_follow'),
]
