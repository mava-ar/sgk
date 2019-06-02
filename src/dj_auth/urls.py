from django.urls import path, re_path
from django.conf import settings
from django.contrib.auth import views as auth_views


urlpatterns = [
    re_path(
        'login/',
        auth_views.LoginView.as_view(template_name='dj_auth/login.html'),
        name='login'),
    re_path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout'),
    re_path(
        r'^password_reset/$',
        auth_views.PasswordResetView.as_view(
            html_email_template_name='dj_auth/password_reset_email.html',
            template_name='dj_auth/password_reset_form.html'),
        name='password_reset'),
    re_path(
        r'^password_reset/done/$',
        auth_views.PasswordResetDoneView.as_view(template_name='dj_auth/password_reset_done.html'),
        name='password_reset_done'),
    re_path(
        r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(template_name='dj_auth/password_reset_confirm.html'),
        name='password_reset_confirm'),
    re_path(
        r'^reset/done/$',
        auth_views.PasswordResetCompleteView.as_view(template_name='dj_auth/password_reset_complete.html'),
        name='password_reset_complete'),
    re_path(
        r'^password_change/$',
        auth_views.PasswordChangeView.as_view(template_name='dj_auth/password_change_form.html'),
        name='password_change'),
    re_path(
        r'^password_change/done/$',
        auth_views.PasswordChangeDoneView.as_view(template_name='dj_auth/password_change_done.html'),
        name='password_change_done'),
]
