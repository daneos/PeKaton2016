import uuid
import json
from django.db import models

class TimeSpan(models.Model):
	id = models.AutoField(primary_key=True)
	time_start = models.DateTimeField()
	time_end = models.DateTimeField()


class User(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100)
	email = models.EmailField()
	password = models.CharField(max_length=40)

	def __str__(self):
		return "id:%d %s" % (self.id, self.name)


class Role(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)
	description = models.CharField(max_length=200)

	def __str__(self):
		return "id:%d %s" % (self.id, self.name)


class Room(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)
	description = models.TextField()
	timetable = models.ManyToManyField(TimeSpan, through='RoomTimetable')

	def __str__(self):
		return "id:%d %s" % (self.id, self.name)


class Group(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)
	members = models.ManyToManyField(User, through='GroupMembership')

	def __str__(self):
		return "id:%d %s" % (self.id, self.name)


class GroupMembership(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	group = models.ForeignKey(Group, on_delete=models.CASCADE)
	role = models.ForeignKey(Role, on_delete=models.CASCADE)

	def __str__(self):
		return "%s/%s/%s" % (self.user.name, self.group.name, self.role.name)


class Event(models.Model):
	id = models.AutoField(primary_key=True)
	time_start = models.DateTimeField()
	time_end = models.DateTimeField()
	name = models.CharField(max_length=50)
	note = models.TextField()
	place_ext = models.CharField(max_length=200)
	place_int = models.ForeignKey(Room, on_delete=models.CASCADE)
	members = models.ManyToManyField(User, through='EventMembership')
	private = models.BooleanField()

	def __str__(self):
		return "id:%d %s" % (self.id, self.name)


class EventMembership(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	event = models.ForeignKey(Event, on_delete=models.CASCADE)
	role = models.ForeignKey(Role, on_delete=models.CASCADE)


class Comment(models.Model):
	id = models.AutoField(primary_key=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	text = models.TextField()

	def __str__(self):
		return str(self.id)


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
		return "id:%d %s" % (self.id, self.name)


class TaskMembership(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	task = models.ForeignKey(Task, on_delete=models.CASCADE)
	role = models.ForeignKey(Role, on_delete=models.CASCADE)


class ParkSpot(models.Model):
	id = models.AutoField(primary_key=True)
	location = models.CharField(max_length=50)
	free = models.BooleanField()

	def __str__(self):
		return "id:%d %s" % (self.id, self.location)


class Session(models.Model):
	id = models.AutoField(primary_key=True)
	time_start = models.DateTimeField(auto_now_add=True)
	last_activity = models.DateTimeField(auto_now_add=True)
	active = models.BooleanField(default=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	session_hash = models.UUIDField(default=uuid.uuid4)

	def __str__(self):
		return "id:%d %s" % (self.id, str(self.session_hash))


class RoomTimetable(models.Model):
	id = models.AutoField(primary_key=True)
	room = models.ForeignKey(Room, on_delete=models.CASCADE)
	timespan = models.ForeignKey(TimeSpan, on_delete=models.CASCADE)
	owner = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.id)


class UserTimetable(models.Model):
	id = models.AutoField(primary_key=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	timespan = models.ForeignKey(TimeSpan, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.id)


class FoodTicket(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)
	description = models.TextField()
	code = models.CharField(max_length=50)
	thumb = models.URLField()

	def __str__(self):
		return "id:%d %s" % (self.id, self.name)
