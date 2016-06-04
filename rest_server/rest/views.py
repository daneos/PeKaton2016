from datetime import datetime
from django.shortcuts import get_object_or_404

from rest.models import *
from rest.serializers import *
from rest.utils import *


def login(rq):
	user = User.objects.get(email=rq.GET.get("email", None))
	if user.password == rq.GET.get("password", None):
		session = Session(user=user)
		session.save()
		return response("OK", SessionSerializer(session))
	else:
		return response("ERROR", "Invalid user details.")


def user(rq, sessid, uid=None):
	if validate_sessid(sessid):
		if uid is None:
			return response("OK", [ UserSerializer(u) for u in User.objects.all() ])
		else:
			return response("OK", UserSerializer(get_object_or_404(User, pk=uid)))
	else:
		return session_expired()


def room(rq, sessid, rid=None):
	if validate_sessid(sessid):
		if rid is None:
			return response("OK", [ RoomSerializer(r) for r in Room.objects.all() ])
		else:
			return response("OK", RoomSerializer(get_object_or_404(Room, pk=rid), detail_mode=True))
	else:
		return session_expired()


def room_register(rq, sessid, rid):
	if validate_sessid(sessid):
		session = get_object_or_404(Session, session_hash=sessid)
		user = session.user
		try:
			time_start = datetime.fromtimestamp(float(rq.GET.get("start")))
			time_end = datetime.fromtimestamp(float(rq.GET.get("end")))
		except:
			time_start = None
			time_end = None
		room = get_object_or_404(Room, pk=rid)
		if time_start and time_end:
			timespan = TimeSpan(time_start=time_start, time_end=time_end)
			timespan.save()
			timetable = RoomTimetable(room=room, timespan=timespan, owner=user)
			timetable.save()
			return response("OK", "Room reserved.")
		else:
			return response("ERROR", "Start time and end time is required.")
	else:
		return session_expired()

def parkspot(rq, sessid, pid=None):
	if validate_sessid(sessid):
		return response("OK", [ ParkSpotSerializer(p) for p in ParkSpot.objects.all() ])
	else:
		return session_expired()


def parkspot_take(rq, sessid, pid):
	if validate_sessid(sessid):
		spot = get_object_or_404(ParkSpot, pk=pid)
		spot.free = False
		spot.save()
		return response("OK", "Park spot taken.")
	else:
		return session_expired()

def parkspot_free(rq, sessid, pid):
	if validate_sessid(sessid):
		spot = get_object_or_404(ParkSpot, pk=pid)
		spot.free = True
		spot.save()
		return response("OK", "Park spot freed.")
	else:
		return session_expired()


def food(rq, sessid, tid=None):
	if validate_sessid(sessid):
		if tid is None:
			return response("OK", [ FoodTicketSerializer(t) for t in FoodTicket.objects.all() ])
		else:
			return response("OK", FoodTicketSerializer(get_object_or_404(FoodTicket, pk=tid), detail_mode=True))
	else:
		return session_expired()


def group(rq, sessid, gid=None):
	if validate_sessid(sessid):
		if gid is None:
			return response("OK", [ GroupSerializer(g) for g in Group.objects.all() ])
		else:
			return response("OK", GroupSerializer(get_object_or_404(Group, pk=gid), detail_mode=True))
	else:
		return session_expired()

