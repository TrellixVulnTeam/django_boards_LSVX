from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('settings/change_password/',
         auth_views.PasswordChangeView.as_view(template_name='accounts/change_password.html'),
         name='change_password'),
    path('settings/change_password_done/',
         auth_views.PasswordChangeDoneView.
         as_view(template_name='accounts/password_change_done.html'),
         name='password_change_done'),
    path('account', views.UserUpdateView.as_view(), name='my_account'),

]
