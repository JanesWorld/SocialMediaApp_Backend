from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["content", "image", "video"]
        widgets = {
            "content": forms.Textarea(attrs={"placeholder": "What's on your mind?"}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={"placeholder": "Write a comment..."}),
        }
