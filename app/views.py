from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.db.models import Q

from .models import Category, LikePost, Post, Comment, SeeLater, LikeComment, User
from .forms import PostForm, CommentForm
from account.models import Follower

"""VIDEO CRUD"""
def create_video_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect(reverse_lazy('my_videos'))
    else:
        form = PostForm()
    return render(request, 'video/create_video.html', {'form':form})

def update_video_view(request, pk):
    video = get_object_or_404(Post, pk=pk)
    form = PostForm(request.POST or None, request.FILES or None, instance=video)
    if form.is_valid():
        form.save()
        return redirect(reverse_lazy('my_videos'))
    return render(request, 'video/update_video.html', {'form': form})

def see(request, pk):
    is_liked_post = is_user = see_later = is_followed = None
    video = Post.objects.get(id=pk)
    video.views += 1
    video.save()
    videos = Post.objects.all()
    likes = LikePost.objects.filter(post=video).count()
    if request.user.is_authenticated:
        is_liked_post = LikePost.objects.filter(post=video, user=request.user).exists()
        is_user = video.user == request.user
        see_later = not SeeLater.objects.filter(post=video, user=request.user).exists()
        is_followed = Follower.objects.filter(follow=video.user, user=request.user).exists()
        print(is_followed)
    comments = []
    comms = Comment.objects.filter(post=video, parent=None)
    for comm in comms:
        comments.append((comm, request.user in map(lambda x:x.user ,comm.likes.all()), LikeComment.objects.filter(comment=comm).count()))
    comment_form = CommentForm()
    return render(request, 'video/stream_video.html', {'video':video, 
                                                       'videos':videos,
                                                       'likes':likes,
                                                       'comments':comments,
                                                       'comment_form':comment_form,
                                                       'is_liked_post':is_liked_post,
                                                       'is_user':is_user,
                                                       'see_later':see_later,
                                                       'is_followed':is_followed})

def my_posts(request):
    videos = request.user.posts.all()
    return render(request, 'video/video_list.html', locals())

def search_video(request, category=None):
    videos = Post.objects.all()
    users = None
    if category:
        cat = get_object_or_404(Category, title=category)
        videos = videos.filter(category=cat)
    search = request.GET.get('q')
    if search:
        videos = videos.filter(Q(title__icontains=search) | Q(description__icontains=search))
        users = User.objects.filter(email__icontains=search)

    return render(request, 'video/video_list.html', {'videos': videos, 'category':category, 'users':users})


"""LIKE"""
def toggle_like_post(request, pk):
    video = Post.objects.get(id=pk)
    like = LikePost.objects.filter(user=request.user, post=video)
    if like.exists(): like.delete()
    else: LikePost.objects.create(user=request.user, post=video)
    return redirect(reverse('see', kwargs={'pk':pk}))

def toggle_like_comment(request, post_id, pk):
    video = Comment.objects.get(id=pk)
    like = LikeComment.objects.filter(user=request.user, comment=video)
    if like.exists(): like.delete()
    else: LikeComment.objects.create(user=request.user, comment=video)
    return redirect(reverse('see', kwargs={'pk':post_id}))

def my_likes(request):
    videos = [i.post for i in request.user.post_likes.all()]
    return render(request, 'video/video_list.html', {'videos': videos})


"""COMMENTS"""
def add_comment(request, pk):
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment_form.save(request, Post.objects.get(id=pk))
        return redirect(reverse_lazy('see', kwargs={"pk":pk}))


"""SEE LATER"""
def add_see_later(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if not SeeLater.objects.filter(user=request.user, post=post).exists():
        SeeLater.objects.create(user=request.user, post=post)
    return redirect(reverse_lazy('see', kwargs={"pk":post.id}))

def see_later_list(request):
    videos = [i.post for i in request.user.see_later.all()]
    return render(request, 'video/video_list.html', {'videos':videos})
