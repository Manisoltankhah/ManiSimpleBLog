from django import forms
from blog.models import Blog
from .models import BlogComments


class EditPostForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'short_description', 'image', 'main_text']

        widgets = {
            'image': forms.FileInput(attrs={
                'placeholder': 'Post Image'}),

            'title': forms.TextInput(attrs={
                'placeholder': 'Title'}),

            'short_description': forms.TextInput(attrs={
                'placeholder': 'Description'}),

            'main_text': forms.Textarea(attrs={
                'rows': '6'})
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = BlogComments
        fields = ['text']
        widgets = {
            'text': forms.TextInput({
                "placeholder": "Comment Here..."
            })
        }
        labels = {
            "text": ""
        }