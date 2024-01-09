from django.template.context_processors import static
from django.urls import path
from . import views

urlpatterns = [
    # path('user-panel-dashboard/', views.UserPanelDashboardPage.as_view(), name='user_panel_dashboard'),
    path('register/', views.RegisterView.as_view(), name='register_page'),
    path('login/', views.LoginView.as_view(), name='login-page'),

]