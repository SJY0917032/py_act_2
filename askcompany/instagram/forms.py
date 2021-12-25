from django import forms
from django.forms import widgets
from .models import Post, Comment

# 폼에서 입력한 fields는 폼에서만 담당한다
# 나머지는 view단에서 책임을짐.

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['photo', 'caption', 'location']
        widgets = {
            "caption" : forms.Textarea
        }
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['message']
        widgets = {
            'message' : forms.Textarea(attrs={'rows' : 3})
        }