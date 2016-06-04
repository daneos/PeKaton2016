import json
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from rest.models import *

def response(data):
	return HttpResponse(json.dumps(data), content_type="application/json")


def login(rq):
	user = get_object_or_404(User, email=rq.GET.get("email", None))
	if user.password == rq.GET.get("password", None):
		session = Session(user=user)
		session.save()
		return response({
			"status": "OK",
			"session_id": str(session.session_hash)
		})
	else:
		return response({
			"status": "ERROR",
			"reason": "Invalid user details."
		})

def room_list(rq, sessid):
	session = get_object_or_404(Session, session_hash=sessid)
	if session.active:
		serialized = [ RoomSerializer(r) for r in Room.objects.all() ]
		return response({
			"status":"OK",
			"data": serialized
		})
	else:
		return response({
			"status": "ERROR",
			"reason": "Session expired."
		})


