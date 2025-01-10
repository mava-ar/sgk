from django.urls import re_path, path
from django.contrib.auth import views as auth_views


urlpatterns = [
    path(
        'login/',
        auth_views.LoginView.as_view(template_name='dj_auth/login.html'),
        name='login'),
    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout'),
    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(
            html_email_template_name='dj_auth/password_reset_email.html',
            template_name='dj_auth/password_reset_form.html'),
        name='password_reset'),
    path(
        'password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(template_name='dj_auth/password_reset_done.html'),
        name='password_reset_done'),
    path(
        'reset/<str:uidb64>/<str:token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name='dj_auth/password_reset_confirm.html'),
        name='password_reset_confirm'),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(template_name='dj_auth/password_reset_complete.html'),
        name='password_reset_complete'),
    path(
        'password_change/',
        auth_views.PasswordChangeView.as_view(template_name='dj_auth/password_change_form.html'),
        name='password_change'),
    path(
        'password_change/done/',
        auth_views.PasswordChangeDoneView.as_view(template_name='dj_auth/password_change_done.html'),
        name='password_change_done'),
]
