from django.template.context_processors import static
from django.urls import path
from user_panel import views

urlpatterns = [
    path('user-panel-dashboard/', views.UserPanelDashboardPage.as_view(), name='user_panel_dashboard'),
    path('edit-user-info/', views.EditUserInfo.as_view(), name='edit_user_info'),
    path('create-post/', views.CreatePost.as_view(), name='create_post'),
    path('change-password/', views.ChangePassword.as_view(), name='change-password'),
    path('logout/', views.Logout.as_view(), name='logout'),
]