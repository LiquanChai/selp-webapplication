# coding:utf-8
'''

'''
from django.conf.urls import patterns, include, url
from usermgt.views import *
from django.contrib.auth import views as auth_views

urlpatterns = patterns('',
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='auth_login'),
    url(regex=r'^register/$', view=RegistrationView.as_view(), name='usermgt_register'),
	url(r'^change_passwd/$', auth_views.password_change, {'template_name': 'changepwd.html'}, name='password_change'),
	url(r'^change_passwd_done/$', auth_views.password_change_done, {'template_name': 'password_change_done.html'}, name='password_change_done'),
	url(r'^logout/$', auth_views.logout, {'template_name': 'logout.html'}, name='auth_logout'),
	url(r'^profile/$', usermgt_profile),
)

