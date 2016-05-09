from django.conf.urls import url, include

from django.contrib.auth import views


urlpatterns = [
    url(r'^logout/', views.logout_then_login, name='logout'),
    url(r'^login/$', views.login, {'template_name': 'dj_auth/login.html'}, name='login'),
    url(r'^password_change/$', views.password_change, {'template_name': 'dj_auth/password_change_form.html'},
        name='password_change'),
    url(r'^password_change/done/$', views.password_change_done, {'template_name': 'dj_auth/password_change_done.html'},
        name='password_change_done'),
    url(r'^password_reset/$', views.password_reset, {
            'html_email_template_name': 'dj_auth/password_reset_email.html',
            'template_name': 'dj_auth/password_reset_form.html'
        }, name='password_reset'),
    url(r'^password_reset/done/$', views.password_reset_done, {'template_name': 'dj_auth/password_reset_done.html'},
        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.password_reset_confirm, {'template_name': 'dj_auth/password_reset_confirm.html'},
        name='password_reset_confirm'),
    url(r'^reset/done/$', views.password_reset_complete, {'template_name': 'dj_auth/password_reset_complete.html'},
        name='password_reset_complete'),
]
