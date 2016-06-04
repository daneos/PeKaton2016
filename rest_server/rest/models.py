import uuid
from django.db import models

class User(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100)
	email = models.EmailField()
	password = models.CharField(max_length=40)


class Role(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)
	description = models.CharField(max_length=200)


class Room(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)
	description = models.TextField()


class Group(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)
	members = models.ManyToManyField(User, through='GroupMembership')


class GroupMembership(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	group = models.ForeignKey(Group, on_delete=models.CASCADE)
	role = models.ForeignKey(Role, on_delete=models.CASCADE)


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


class EventMembership(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	event = models.ForeignKey(Event, on_delete=models.CASCADE)
	role = models.ForeignKey(Role, on_delete=models.CASCADE)


class Task(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)
	description = models.TextField()
	time_start = models.DateTimeField()
	deadline = models.DateTimeField()
	done = models.PositiveSmallIntegerField()
	members = models.ManyToManyField(User, through="TaskMembership")


class TaskMembership(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	task = models.ForeignKey(Task, on_delete=models.CASCADE)
	role = models.ForeignKey(Role, on_delete=models.CASCADE)


class ParkSpot(models.Model):
	id = models.AutoField(primary_key=True)
	location = models.CharField(max_length=50)
	free = models.BooleanField()


class Session(models.Model):
	id = models.AutoField(primary_key=True)
	time_start = models.DateTimeField(auto_now_add=True)
	last_activity = models.DateTimeField(auto_now_add=True)
	active = models.BooleanField(default=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	session_hash = models.UUIDField(default=uuid.uuid4)