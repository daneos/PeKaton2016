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
# import jqchat.urls

base_url = r"^api/rest/v1"
session = r"(?P<sessid>[0-9a-f\-]+)"

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^chat/', include(jqchat.urls)),

    url(r'%s/login' % base_url,										'rest.views.login'),
    url(r'%s/logout/%s/$' % (base_url,session),						'rest.views.logout'),
    url(r'%s/users/%s/$' % (base_url,session),						'rest.views.user'),
    url(r'%s/users/%s/(?P<uid>\d+)/$' % (base_url,session),			'rest.views.user'),
    url(r'%s/users/%s/(?P<uid>\d+)/kudos/' % (base_url,session),	'rest.views.user_kudos'),
    url(r'%s/rooms/%s/$' % (base_url,session),						'rest.views.room'),
    url(r'%s/rooms/%s/(?P<rid>\d+)/$' % (base_url,session),			'rest.views.room'),
    url(r'%s/rooms/%s/(?P<rid>\d+)/register' % (base_url,session),	'rest.views.room_register'),
    url(r'%s/parkspots/%s/$' % (base_url,session),					'rest.views.parkspot'),
    url(r'%s/parkspots/%s/(?P<pid>\d+)/take/$' % (base_url,session),'rest.views.parkspot_take'),
    url(r'%s/parkspots/%s/(?P<pid>\d+)/free/$' % (base_url,session),'rest.views.parkspot_free'),
    url(r'%s/food/%s/$' % (base_url,session),						'rest.views.food'),
    url(r'%s/food/%s/(?P<tid>\d+)/$' % (base_url,session),			'rest.views.food'),
    url(r'%s/groups/%s/$' % (base_url,session),						'rest.views.group'),
    url(r'%s/groups/%s/(?P<gid>\d+)/$' % (base_url,session),		'rest.views.group'),
    url(r'%s/tasks/%s/$' % (base_url,session),						'rest.views.task'),
    url(r'%s/tasks/%s/(?P<tid>\d+)/$' % (base_url,session),			'rest.views.task'),
    url(r'%s/tasks/%s/add/' % (base_url,session),					'rest.views.task_add'),
    url(r'%s/tasks/%s/(?P<tid>\d+)/update/' % (base_url,session),	'rest.views.task_update'),
    url(r'%s/tasks/%s/(?P<tid>\d+)/comment/' % (base_url,session),	'rest.views.task_comment'),
    url(r'%s/roles/%s/$' % (base_url,session),						'rest.views.role'),
    url(r'%s/roles/%s/(?P<rid>\d+)/$' % (base_url,session),			'rest.views.role'),
    url(r'%s/events/%s/$' % (base_url,session),						'rest.views.event'),
    url(r'%s/events/%s/(?P<eid>\d+)/$' % (base_url,session),		'rest.views.event'),
    url(r'%s/events/%s/add/' % (base_url,session),					'rest.views.event_add'),
    url(r'%s/events/%s/(?P<eid>\d+)/update/' % (base_url,session),	'rest.views.event_update'),
    url(r'%s/events/%s/types/$' % (base_url,session),				'rest.views.event_type'),
    url(r'%s/events/%s/types/(?P<etid>\d+)/$' % (base_url,session),	'rest.views.event_type'),
    url(r'%s/messages/%s/$' % (base_url,session),					'rest.views.message'),
    url(r'%s/messages/%s/(?P<mid>\d+)/$' % (base_url,session),		'rest.views.message'),
    url(r'%s/messages/%s/write/$' % (base_url,session),				'rest.views.message_write'),
]
