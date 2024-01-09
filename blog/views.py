from django.core.checks import messages
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from blog.forms import EditPostForm, CommentForm
from utils.http_service import get_client_ip
from django.views.generic import DetailView, ListView, CreateView, DeleteView
from django.views.generic.base import TemplateView, View
from blog.models import Blog, BlogVisit, BlogComments


class IndexPage(TemplateView):
    template_name = 'blog/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexPage, self).get_context_data()
        latest_posts: Blog = Blog.objects.filter(is_active=True)
        context['latest_posts'] = latest_posts
        return context


class PostDetail(DetailView):
    model = Blog
    template_name = 'blog/post-detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comment_form = CommentForm()
        blog: Blog = kwargs.get('object')
        comments = BlogComments.objects.filter(blog_id=blog.id)
        blog = self.object
        current_user = self.request.user.username
        context['current_user'] = current_user
        user_ip = get_client_ip(self.request)
        user_id = None
        if self.request.user.is_authenticated:
            user_id = self.request.user.id
        had_been_visited = BlogVisit.objects.filter(ip__iexact=user_ip, blog_id=blog.id).exists()
        if not had_been_visited:
            new_visit = BlogVisit(ip=user_ip, user_id=user_id, blog_id=blog.id)
            new_visit.save()
        context['comment_form'] = comment_form
        context['comments'] = comments
        return context


class AllPosts(ListView):
    model = Blog
    template_name = 'blog/all-posts.html'
    context_object_name = 'all_posts'
    paginate_by = 12


class EditPost(View):
    def get(self, request):
        edit_post_form = EditPostForm()
        context = {
            'edit_post_form': edit_post_form
        }
        return render(request, 'blog/edit-post.html', context)

    def post(self, request):
        blog = Blog.objects.filter(id=request.blog.id).first()
        edit_post_form = EditPostForm(instance=blog)
        if edit_post_form.is_valid():
            edit_post_form.save(commit=True)
            return redirect(reverse('home_page'))

        context = {
            'edit_post_form': edit_post_form
        }
        return render(request, 'blog/edit-post.html', context)


class AddComment(CreateView):
    model = BlogComments
    form_class = CommentForm
    template_name = 'blog/post-detail.html'
    context_object_name = 'comment_form'
    success_url = reverse_lazy('posts-page')


    def form_valid(self, form):
        form.instance.blog_id = self.kwargs['pk']
        form.instance.user_id = self.request.user.id
        return super().form_valid(form)



class PostDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('home_page')
    template_name = 'blog/post-delete-confirm.html'
    context_object_name = "post"




