import uuid
import json
from django.db import models

class TimeSpan(models.Model):
	id = models.AutoField(primary_key=True)
	time_start = models.DateTimeField()
	time_end = models.DateTimeField()

	def __str__(self):
		return "TimeSpan id:%d %s-%s" % (self.id, str(self.time_start), str(self.time_end))


class User(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100)
	email = models.EmailField()
	password = models.CharField(max_length=40)
	points = models.IntegerField()
	points_available = models.IntegerField()
	hours = models.FloatField()
	hour_goal = models.FloatField()
	salary = models.FloatField()

	def __str__(self):
		return "User id:%d %s" % (self.id, self.name)

class Message(models.Model):
	id = models.AutoField(primary_key=True)
	from_user_id = models.IntegerField()
	to_user_id = models.IntegerField()
	time = models.DateTimeField(auto_now_add=True)
	text = models.TextField()

	def __str__(self):
		return "Message id:%d %d->%d" % (self.id, self.from_user_id, self.to_user_id)


class Role(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)
	description = models.CharField(max_length=200)

	def __str__(self):
		return "Role id:%d %s" % (self.id, self.name)


class Room(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)
	description = models.TextField()
	timetable = models.ManyToManyField(TimeSpan, through='RoomTimetable')

	def __str__(self):
		return "Room id:%d %s" % (self.id, self.name)


class Group(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)
	members = models.ManyToManyField(User, through='GroupMembership')

	def __str__(self):
		return "Group id:%d %s" % (self.id, self.name)


class GroupMembership(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	group = models.ForeignKey(Group, on_delete=models.CASCADE)
	role = models.ForeignKey(Role, on_delete=models.CASCADE)

	def __str__(self):
		return "GroupMembership %s/%s/%s" % (self.user.name, self.group.name, self.role.name)


class EventType(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)

	def __str__(self):
		return "EventType id:%d %s" % (self.id, self.name)


class Event(models.Model):
	id = models.AutoField(primary_key=True)
	type = models.ForeignKey(EventType, on_delete=models.CASCADE)
	time_start = models.DateTimeField()
	time_end = models.DateTimeField()
	name = models.CharField(max_length=50)
	note = models.TextField()
	place_ext = models.CharField(max_length=200, null=True, blank=True)
	place_int = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, blank=True)
	members = models.ManyToManyField(User, through='EventMembership')
	private = models.BooleanField()

	def __str__(self):
		return "Event id:%d %s" % (self.id, self.name)


class EventMembership(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	event = models.ForeignKey(Event, on_delete=models.CASCADE)
	role = models.ForeignKey(Role, on_delete=models.CASCADE)

	def __str__(self):
		return "EventMembership %s/%s/%s" % (self.user.name, self.event.name, self.role.name)


class Comment(models.Model):
	id = models.AutoField(primary_key=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	text = models.TextField()

	def __str__(self):
		return "Comment id:%d" % self.id


class Task(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)
	description = models.TextField()
	time_start = models.DateTimeField()
	deadline = models.DateTimeField()
	done = models.PositiveSmallIntegerField()
	members = models.ManyToManyField(User, through="TaskMembership")
	comments = models.ManyToManyField(Comment)

	def __str__(self):
		return "Task id:%d %s" % (self.id, self.name)


class TaskMembership(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	task = models.ForeignKey(Task, on_delete=models.CASCADE)
	role = models.ForeignKey(Role, on_delete=models.CASCADE)

	def __str__(self):
		return "TaskMembership %s/%s/%s" % (self.user.name, self.task.name, self.role.name)


class ParkSpot(models.Model):
	id = models.AutoField(primary_key=True)
	location = models.CharField(max_length=50)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	free = models.BooleanField()

	def __str__(self):
		return "ParkSpot id:%d %s" % (self.id, self.location)


class Session(models.Model):
	id = models.AutoField(primary_key=True)
	time_start = models.DateTimeField(auto_now_add=True)
	last_activity = models.DateTimeField(auto_now_add=True)
	active = models.BooleanField(default=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	session_hash = models.UUIDField(default=uuid.uuid4)

	def __str__(self):
		return "Session id:%d %s" % (self.id, str(self.session_hash))


class RoomTimetable(models.Model):
	id = models.AutoField(primary_key=True)
	room = models.ForeignKey(Room, on_delete=models.CASCADE)
	timespan = models.ForeignKey(TimeSpan, on_delete=models.CASCADE)
	owner = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return "RoomTimetable id:%d" % self.id


class UserTimetable(models.Model):
	id = models.AutoField(primary_key=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	timespan = models.ForeignKey(TimeSpan, on_delete=models.CASCADE)

	def __str__(self):
		return "UserTimetable id:%d" % str(self.id)


class FoodTicket(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)
	description = models.TextField()
	code = models.CharField(max_length=50)
	thumb = models.URLField()

	def __str__(self):
		return "FoodTicket id:%d %s" % (self.id, self.name)