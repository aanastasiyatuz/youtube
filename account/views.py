from django.contrib.auth.views import LoginView
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView
from django.urls import reverse_lazy

from .forms import RegistrationForm
from .models import Follower

User = get_user_model()

class RegisterView(CreateView):
    model = User
    template_name = 'register.html'
    form_class = RegistrationForm
    success_url = 'https://mail.google.com'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['register_form'] = self.get_form(self.get_form_class())
        return context

class SignInView(LoginView):
    template_name = 'login.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_form'] = self.get_form(self.get_form_class())
        return context

def activate(request, activation_code):
    user = get_object_or_404(User, activation_code=activation_code)
    user.is_active = True
    user.activation_code = ''
    user.save()
    return redirect(reverse_lazy('login'))

def profile(request, user=None):
    if user is None:
        user = request.user
    else:
        user = get_object_or_404(User, email=user)
    if request.user.is_authenticated:
        is_followed = Follower.objects.filter(follow=user, user=request.user).exists()
    follow = user.followers.all().count()
    followers = Follower.objects.filter(follow=user).count()
    videos = user.posts.all()
    return render(request, 'profile.html', locals())

def follow_create(request, user):
    if Follower.objects.filter(user=request.user, follow=User.objects.get(email=user)).exists():
        Follower.objects.get(user=request.user, follow=User.objects.get(email=user)).delete()
    else:
        Follower.objects.create(user=request.user, follow=User.objects.get(email=user))
    return redirect('my_profile')

def see_follow(request, user):
    user = User.objects.get(email=user)
    followers = Follower.objects.filter(follow=user)
    follow = user.followers.all()
    return render(request, 'follow.html', locals())