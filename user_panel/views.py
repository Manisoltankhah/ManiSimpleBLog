from django.contrib.auth import logout
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView
from blog.models import Blog
from . import forms
from user.models import User
from .forms import EditProfileModelForm, CreatePostForm, ResetPasswordForm


class UserPanelDashboardPage(TemplateView):
    template_name = 'user_panel/user-panel-dashboard.html'
    model = User

    def get_context_data(self, **kwargs):
        context = super(UserPanelDashboardPage, self).get_context_data()
        request = self.request
        current_user = User.objects.filter(id=request.user.id).first()
        context['current_user'] = current_user
        return context


class EditUserInfo(View):
    def get(self, request: HttpRequest):
        current_user = User.objects.filter(id=request.user.id).first()
        edit_form = EditProfileModelForm(instance=current_user)
        context = {
            'edit_form': edit_form,
            'current_user': current_user
        }
        return render(request, 'user_panel/edit-profile.html', context)

    def post(self, request: HttpRequest):
        current_user = User.objects.filter(id=request.user.id).first()
        edit_form = EditProfileModelForm(request.POST, request.FILES, instance=current_user)
        if edit_form.is_valid():
            edit_form.save(commit=True)
            return redirect(reverse('user_panel_dashboard'))

        context = {
            'edit_form': edit_form,
            'current_user': current_user
        }
        return render(request, 'user_panel/edit-profile.html', context)


class CreatePost(View):
    def get(self, request: HttpRequest):
        post_form = CreatePostForm()
        context = {
            'post_form': post_form,
        }
        return render(request, 'user_panel/create-post.html', context)

    def post(self, request: HttpRequest):
        post_form = CreatePostForm(request.POST or None, request.FILES)
        if post_form.is_valid():
            new_post = post_form.save(commit=False)
            new_post.author = self.request.user
            new_post.save()
        context = {
            'post_form': post_form,
        }
        return render(request, 'user_panel/create-post.html', context)


class ChangePassword(View):

    def get(self, request):
        change_password_form = forms.ChangePasswordForm()
        context = {
            'change_password_form': change_password_form
        }
        return render(request, 'user_panel/change-password-page.html', context)

    def post(self, request):
        change_password_form = forms.ChangePasswordForm(request.POST)
        if change_password_form.is_valid():
            current_user = User.objects.filter(id=request.user.id)
            if current_user.check_password(change_password_form.cleaned_data.get('current_password')):
                current_user.set_password(change_password_form.cleaned_data.get('new_password'))
                current_user.save()
                logout(request)
                return redirect(reverse('login-page'))

        context = {
            'change_password_form': change_password_form
        }
        return render(request, 'user_panel/change-password-page.html', context)


class ResetPasswordView(View):

    def get(self, request, active_code):
        user = User.objects.filter(email_active_code__iexact=active_code).first()
        if user is None:
            return redirect(reverse('login_page'))
        reset_pass_form = ResetPasswordForm()
        context = {'reset_pass_form': reset_pass_form,
                   'user': user
                   }
        return render(request, 'user_panel/change-password-page.html', context)

    def post(self, request, active_code):
        reset_pass_form = ResetPasswordForm(request.POST)
        user = User.objects.filter(email_active_code__iexact=active_code).first()
        if reset_pass_form.is_valid():
            if user is None:
                return redirect(reverse('login_page'))
            user_new_password = reset_pass_form.cleaned_data.get('password')
            user.set_password(user_new_password)
            # user.email_active_code = get_random_string(6)
            user.is_active = True
            user.save()
            return redirect(reverse('login_page'))

        context = {
            'reset_pass_form': reset_pass_form,
            'user': user
        }
        return render(request, 'user_panel/change-password-page.html', context)


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('login-page'))