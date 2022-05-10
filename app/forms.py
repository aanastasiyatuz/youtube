from django import forms

from .models import Category, Post, Comment

class PostForm(forms.ModelForm):
    category = forms.CharField()

    class Meta:
        model = Post
        exclude = ('user', 'created_at', 'views', 'category')
    
    def save(self, commit=False):
        if not self.cleaned_data.get('category'):
            return super().save(commit=commit)
        post = self.instance
        category = Category.objects.get_or_create(title=self.cleaned_data.get("category"))[0]
        post.category = category
        return super().save(commit=commit)

class CommentForm(forms.ModelForm):
    body = forms.CharField(label='')

    class Meta:
        model = Comment
        fields = ('body',)
    
    def save(self, request, post):
        comment = self.instance
        comment.user = request.user
        comment.post = post
        return super().save()
