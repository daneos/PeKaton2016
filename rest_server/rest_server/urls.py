"""rest_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
import rest

base_url = r"^api/rest/v1"
session = r"(?P<sessid>[0-9a-f\-]+)"

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url(r'%s/login' % base_url,										'rest.views.login'),
    url(r'%s/users/%s/$' % (base_url,session),						'rest.views.user'),
    url(r'%s/users/%s/(?P<uid>\d+)/' % (base_url,session),			'rest.views.user'),
    url(r'%s/rooms/%s/$' % (base_url,session),						'rest.views.room'),
    url(r'%s/rooms/%s/(?P<rid>\d+)/$' % (base_url,session),			'rest.views.room'),
    url(r'%s/rooms/%s/(?P<rid>\d+)/register' % (base_url,session),	'rest.views.room_register'),
    url(r'%s/parkspots/%s/$' % (base_url,session),					'rest.views.parkspot'),
    url(r'%s/parkspots/%s/(?P<pid>\d+)/take$' % (base_url,session),	'rest.views.parkspot_take'),
    url(r'%s/parkspots/%s/(?P<pid>\d+)/free$' % (base_url,session),	'rest.views.parkspot_free'),
    url(r'%s/food/%s/$' % (base_url,session),						'rest.views.food'),
    url(r'%s/food/%s/(?P<tid>\d+)/' % (base_url,session),			'rest.views.food'),
    url(r'%s/groups/%s/$' % (base_url,session),						'rest.views.group'),
    url(r'%s/groups/%s/(?P<gid>\d+)/' % (base_url,session),			'rest.views.group'),



]
