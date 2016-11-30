from django.conf.urls import url, include

import django.contrib.auth.views
from . import views
from .forms import LoginForm

urlpatterns = [
	#test page
	url(r'^$', views.navigate, name='navigate'),
    url(r'^index$', views.index, name='index'),
    # Route for built-in authentication with our own custom login page
    url(r'^login$', django.contrib.auth.views.login, {'template_name':'travelapp/signin.html','authentication_form':LoginForm}, name='login'),
	# Route to logout a user and send them back to the login page
    url(r'^logout$', django.contrib.auth.views.logout_then_login, name='logout'),
    url(r'^register$', views.register, name='register'),
    url(r'^add$', views.add, name='add'),
    url(r'^plan_result$', views.plan_result, name='plan_result'),
    url(r'^tour_pal$', views.tour_pal, name='tour_pal'),
    url(r'^add_comment/(?P<id>\d+)$', views.add_comment, name = 'comment'),
    url(r'^edit_profile', views.edit_profile, name='edit_profile'),
    url(r'^profile/(?P<id>\d+)$', views.profile, name='profile'),
    url(r'^profile$', views.my_profile, name='my_profile'),
    url(r'^review/(?P<id>\d+)$', views.add_review, name='review'),
    url(r'^icon/(?P<id>\d+)$', views.icon, name='icon'),
    url(r'^blog$', views.blog, name='blog'),
    url(r'^new_blog$', views.new_blog, name='new_blog'),
    url(r'^search$', views.search, name='search'),
    url(r'^delete_event/(?P<id>\d+)$', views.delete_event, name='delete_event'),
    url(r'^delete_plan/(?P<id>\d+)$', views.delete_plan, name='delete_plan'),
    
]

