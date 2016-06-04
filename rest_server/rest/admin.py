from django.contrib import admin
from rest.models import *

from django.db import models

admin.site.register(User)
admin.site.register(Role)
admin.site.register(Room)
admin.site.register(Group)
admin.site.register(GroupMembership)
admin.site.register(Event)
admin.site.register(Task)
admin.site.register(ParkSpot)
admin.site.register(Session)
admin.site.register(RoomTimetable)
admin.site.register(UserTimetable)
admin.site.register(TimeSpan)
admin.site.register(FoodTicket)

