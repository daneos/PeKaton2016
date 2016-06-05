from django.contrib import admin
from rest.models import *

from django.db import models

admin.sites.AdminSite.site_header = "Company management REST interface administration"
admin.sites.AdminSite.site_title = "Application administration"

admin.site.register(User)
admin.site.register(Role)
admin.site.register(Room)
admin.site.register(Group)
admin.site.register(GroupMembership)
admin.site.register(Event)
admin.site.register(EventMembership)
admin.site.register(EventType)
admin.site.register(Task)
admin.site.register(ParkSpot)
admin.site.register(Session)
admin.site.register(RoomTimetable)
admin.site.register(UserTimetable)
admin.site.register(TimeSpan)
admin.site.register(FoodTicket)
admin.site.register(TaskMembership)
admin.site.register(Comment)
admin.site.register(Message)