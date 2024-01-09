from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexPage.as_view(), name='home_page'),
    path('posts', views.AllPosts.as_view(), name='posts-page'),
    path('posts/<slug:slug>', views.PostDetail.as_view(), name='post-detail-page'),
    path('posts/<int:pk>/add-comment', views.AddComment.as_view(), name='add_blog_comment'),
    path('edit-post', views.EditPost.as_view(), name='edit-post-page'),
    path('posts/<int:pk>/delete-post/', views.PostDeleteView.as_view(), name='delete-post'),
]
