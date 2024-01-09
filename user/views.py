from django.contrib.auth import login
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.views import View
from django.views.generic import TemplateView

from user.forms import RegisterForm, LoginForm
from user.models import User


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        # print(f'random string: {get_random_string(6)}')
        context = {
            "register_form": register_form
        }
        return render(request, 'user/register-page.html', context)

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_email = register_form.cleaned_data.get('email')
            user_password = register_form.cleaned_data.get('password')
            user: bool = User.objects.filter(email__iexact=user_email).exists()
            if user:
                register_form.add_error('email', 'email had been used')
            else:
                new_user = User(email=user_email, email_active_code=get_random_string(6), is_active=True, username=user_email)
                new_user.set_password(user_password)
                new_user.save()
                # email_to_user = EmailMessage('فعال سازی حساب کاربری', f'''http://127.0.0.1:8080/activate-account/{new_user.email_active_code}''', to=[f'{new_user.email}'])
                # email_to_user.send()
                return redirect(reverse('login-page'))

        context = {
              "register_form": register_form
        }
        return render(request, 'user/register-page.html', context)


class LoginView(View):

    def get(self, request):
        login_form = LoginForm()
        context = {
            "login_form": login_form
        }
        return render(request, 'user/login-page.html', context)

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_email = login_form.cleaned_data.get('email')
            user_password = login_form.cleaned_data.get('password')
            user: User = User.objects.filter(email__iexact=user_email).first()
            if user is not None:
                if not user.is_active:
                    login_form.add_error('email', 'حساب کاربری فعال نشده')
                else:
                    is_password_correct = user.check_password(user_password)
                    if is_password_correct:
                        login(request, user)
                        return redirect(reverse('home_page'))

        context = {
             "login_form": login_form
        }
        return render(request, 'user/login-page.html', context)


