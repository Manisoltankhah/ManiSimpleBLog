from django import forms
from django.core import validators
from django.core.exceptions import ValidationError


class RegisterForm(forms.Form):
    email = forms.EmailField(
        label='Email:',
        widget=forms.EmailInput(attrs={'placeholder': 'Email'}),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )

    username = forms.CharField(
        label='Username:',
        widget=forms.TextInput(attrs={'placeholder': 'Username'}),
        validators=[
            validators.MaxLengthValidator(100)
        ]
    )

    password = forms.CharField(
        label='Password:',
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        validators=[
            validators.MaxLengthValidator(100)
        ]
    )

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password == confirm_password:
            return confirm_password
        raise ValidationError('password and confirm password are not the same')


class LoginForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'placeholder': 'Email'}),
        validators=[
            validators.MaxLengthValidator(100),
            validators.EmailValidator,
        ]
    )

    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        validators=[
            validators.MaxLengthValidator(100)
        ]
    )