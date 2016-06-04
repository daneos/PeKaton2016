from django.contrib import admin
from rest import *

from django.db import models

class UserAdmin(models.ModelAdmin):
	pass

class RoleAdmin(models.ModelAdmin):
	pass

class RoomAdmin(models.ModelAdmin):
	pass

class GroupAdmin(models.ModelAdmin):
	pass

class GroupMembershipAdmin(models.ModelAdmin):
	pass

class EventAdmin(models.ModelAdmin):
	pass

class TaskAdmin(models.ModelAdmin):
	pass

class ParkSpotAdmin(models.ModelAdmin):
	pass



admin.site.register(User, UserAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(GroupMembership, GroupMembershipAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(ParkSpot, ParkSpotAdmin)

