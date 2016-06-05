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

def logout(rq, sessid):
	if validate_sessid(sessid):
		session = get_object_or_404(Session, session_hash=sessid)
		session.active = False
		session.save()
		return response("OK", "Logged out succesfully.")
	else:
		return session_expired()


def user(rq, sessid, uid=None):
	if validate_sessid(sessid):
		if uid is None:
			return response("OK", [ UserSerializer(u) for u in User.objects.all() ])
		else:
			return response("OK", UserSerializer(get_object_or_404(User, pk=uid), detail_mode=True))
	else:
		return session_expired()


def user_kudos(rq, sessid, uid):
	if validate_sessid(sessid):
		kudos = rq.GET.get("points", None)
		print kudos
		if kudos:
			kudos = int(kudos)
			session = get_object_or_404(Session, session_hash=sessid)
			current_user = session.user
			print current_user.points_available
			if current_user.points_available >= kudos:
				kudos_user = get_object_or_404(User, pk=uid)
				kudos_user.points += kudos
				current_user.points_available -= kudos
				kudos_user.save()
				current_user.save()
				return response("OK", "User %d gave user %d %d kudos points." % (current_user.id, kudos_user.id, kudos))
			else:
				return response("ERROR", "You don't have enough points to give.")
		else:
			return response("ERROR", "You must provide amount of points.")
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
			return response("OK", "Room %s reserved." % room.name)
		else:
			return response("ERROR", "Start time and end time is required.")
	else:
		return session_expired()

def parkspot(rq, sessid):
	if validate_sessid(sessid):
		return response("OK", [ ParkSpotSerializer(p) for p in ParkSpot.objects.all() ])
	else:
		return session_expired()


def parkspot_take(rq, sessid, pid):
	if validate_sessid(sessid):
		spot = get_object_or_404(ParkSpot, pk=pid)
		session = get_object_or_404(Session, session_hash=sessid)
		spot.user = session.user
		spot.free = False
		spot.save()
		return response("OK", "Park spot %s taken." % spot.location)
	else:
		return session_expired()

def parkspot_free(rq, sessid, pid):
	if validate_sessid(sessid):
		spot = get_object_or_404(ParkSpot, pk=pid)
		spot.user = None
		spot.free = True
		spot.save()
		return response("OK", "Park spot %s freed." % spot.location)
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
			return response("OK", GroupSerializer(get_object_or_404(Group, pk=gid)))
	else:
		return session_expired()


def task(rq, sessid, tid=None):
	if validate_sessid(sessid):
		if tid is None:
			return response("OK", [ TaskSerializer(t) for t in Task.objects.all() ])
		else:
			return response("OK", TaskSerializer(get_object_or_404(Task, pk=tid), detail_mode=True))
	else:
		return session_expired()


def task_add(rq, sessid):
	if validate_sessid(sessid):
		task = Task(
			name=rq.GET.get("name"),
			description=rq.GET.get("description"),
			time_start=datetime.fromtimestamp(float(rq.GET.get("start"))),
			deadline=datetime.fromtimestamp(float(rq.GET.get("deadline"))),
			done=0
		)
		task.save()
		return response("OK", "Task %d added." % task.id)
	else:
		return session_expired()


def task_update(rq, sessid, tid):
	if validate_sessid(sessid):
		name = rq.GET.get("name", None)
		description = rq.GET.get("description", None)
		try:
			deadline = datetime.fromtimestamp(float(rq.GET.get("deadline", None)))
		except:
			deadline = None
		done = rq.GET.get("done", None)
		add_member = rq.GET.get("add_member", None)

		task = get_object_or_404(Task, pk=tid)
		if name:
			task.name = name
		if description:
			task.description = description
		if deadline:
			task.deadline = deadline
		if done:
			task.done = done
		if add_member:
			role = rq.GET.get("role", None)
			if role:
				membership = TaskMembership(
					task=task,
					user=get_object_or_404(User, pk=add_member),
					role=get_object_or_404(Role, pk=role)
				)
				membership.save()
			else:
				return response("ERROR", "When adding member you must specify role.")
		task.save()
		return response("OK", "Task %d updated." % task.id)
	else:
		return session_expired()


def task_comment(rq, sessid, tid):
	if validate_sessid(sessid):
		session = get_object_or_404(Session, session_hash=sessid)
		task = get_object_or_404(Task, pk=tid)
		user = session.user
		comment = Comment(user=user, text=rq.GET.get("text"))
		comment.save()
		task.comments.add(comment)
		task.save()
		return response("OK", "Comment %d saved." % comment.id)
	else:
		return session_expired()

def role(rq, sessid, rid=None):
	if validate_sessid(sessid):
		if rid is None:
			return response("OK", [ RoleSerializer(r) for r in Role.objects.all() ])
		else:
			return response("OK", RoleSerializer(get_object_or_404(Role, pk=rid)))
	else:
		return session_expired()

def event(rq, sessid, eid=None):
	if validate_sessid(sessid):
		if eid is None:
			return response("OK", [ EventSerializer(e) for e in Event.objects.all() ])
		else:
			return response("OK", EventSerializer(get_object_or_404(Event, pk=eid), detail_mode=True))
	else:
		return session_expired()

def event_add(rq, sessid):
	if validate_sessid(sessid):
		place_ext = rq.GET.get("place_ext", None)
		place_int = rq.GET.get("place_int", None)
		if place_int:
			place_int = get_object_or_404(Room, pk=place_int)
		private = rq.GET.get("private")
		if private == "true":
			private = True
		else:
			private = False
		event = Event(
			name=rq.GET.get("name"),
			note=rq.GET.get("note"),
			time_start=datetime.fromtimestamp(float(rq.GET.get("start"))),
			time_end=datetime.fromtimestamp(float(rq.GET.get("end"))),
			place_int=place_int,
			place_ext=place_ext,
			private=private,
			type=get_object_or_404(EventType, pk=rq.GET.get("type"))
		)
		event.save()
		return response("OK", "Event %d added." % event.id)
	else:
		return session_expired()

def event_update(rq, sessid, eid):
	if validate_sessid(sessid):
		name = rq.GET.get("name", None)
		note = rq.GET.get("note", None)
		try:
			time_start = datetime.fromtimestamp(float(rq.GET.get("start", None)))
		except:
			time_start = None
		try:
			time_end = datetime.fromtimestamp(float(rq.GET.get("end", None)))
		except:
			time_end = None
		place_ext = rq.GET.get("place_ext", None)
		place_int = rq.GET.get("place_int", None)
		if place_int:
			place_int = get_object_or_404(Room, pk=place_int)
		private = rq.GET.get("private")
		if private == "true":
			private = True
		else:
			private = False
		etype = rq.GET.get("type", None)
		add_member = rq.GET.get("add_member", None)

		event = get_object_or_404(Event, pk=eid)
		if name:
			event.name = name
		if note:
			event.note = note
		if time_start:
			event.time_start = time_start
		if time_end:
			event.time_end = time_end
		if place_int:
			event.place_int = place_int
		if place_ext:
			event.place_ext = place_ext
		if private is not None:
			event.private = private
		if etype:
			event.type = get_object_or_404(EventType, pk=etype)

		if add_member:
			role = rq.GET.get("role", None)
			if role:
				membership = EventMembership(
					event=event,
					user=get_object_or_404(User, pk=add_member),
					role=get_object_or_404(Role, pk=role)
				)
				membership.save()
			else:
				return response("ERROR", "When adding member you must specify role.")
		event.save()
		return response("OK", "Event %d updated." % event.id)
	else:
		return session_expired()

def event_type(rq, sessid, etid=None):
	if validate_sessid(sessid):
		if etid is None:
			return response("OK", [ EventTypeSerializer(et) for et in EventType.objects.all() ])
		else:
			return response("OK", EventTypeSerializer(get_object_or_404(EventType, pk=etid)))
	else:
		return session_expired()

def message(rq, sessid, mid=None):
	if validate_sessid(sessid):
		session = get_object_or_404(Session, session_hash=sessid)
		if mid is None:
			return response("OK", [ MessageSerializer(m) for m in Message.objects.filter(to_user_id=session.user.id)[:10] ])
		else:
			return response("OK", MessageSerializer(get_object_or_404(Message, pk=mid)))
	else:
		return session_expired()

def message_write(rq, sessid):
	if validate_sessid(sessid):
		session = get_object_or_404(Session, session_hash=sessid)
		message = Message(
			from_user_id=session.user.id,
			to_user_id=rq.GET.get("to"),
			text=rq.GET.get("text")
		)
		message.save()
		return response("OK", "Message %d sent." % message.id)
	else:
		return session_expired()

def time_start(rq, sessid):
	if validate_sessid(sessid):
		session = get_object_or_404(Session, session_hash=sessid)
		session.user.logtime = datetime.datetime.now()
		session.user.save()
		return response("OK", "Time logging started.")
	else:
		return session_expired()

def time_stop(rq, sessid):
	if validate_sessid(sessid):
		session = get_object_or_404(Session, session_hash=sessid)
		diff = datetime.datetime.now() - session.user.logtime
		session.user.hours += diff.total_seconds()/3600
		session.user.save()
		return response("OK", "Time logging stopped.")
	else:
		return session_expired()