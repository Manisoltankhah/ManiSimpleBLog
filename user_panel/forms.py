from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from blog.models import Blog
from user.models import User


class EditProfileModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'profile_picture', 'about_user']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'first name'}),

            'last_name': forms.TextInput(attrs={
                'placeholder': 'last name'}),

            'profile_picture': forms.FileInput(attrs={
                'placeholder': 'profile picture'}),

            'about_user': forms.Textarea(attrs={
                'rows': '6'})
        }


class CreatePostForm(forms.ModelForm):
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


class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Current Password'}))

    new_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'New Password'})
    )


class ResetPasswordForm(forms.Form):
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
        validators=[
            validators.MaxLengthValidator(100)
        ]
    )

    confirm_password = forms.CharField(
        label='Confirm_password',
        widget=forms.PasswordInput(),
        validators=[
            validators.MaxLengthValidator(100)
        ]
    )