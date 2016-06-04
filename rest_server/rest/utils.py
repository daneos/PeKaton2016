import json
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from rest.models import *

def response(status, data):
	body = {"status": status}
	if status == "ERROR":
		body["reason"] = data
	else:
		body["data"] = data
	return HttpResponse(json.dumps(body), content_type="application/json")

def validate_sessid(sessid):
	session = get_object_or_404(Session, session_hash=sessid)
	return session.active

def session_expired():
	return response("ERROR", "Session expired.")