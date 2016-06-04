from rest.models import *

def UserSerializer(u):
	data = {}
	data['id'] = u.id
	data['name'] = u.name
	data['email'] = u.email
	return data

def RoomSerializer(r, detail_mode=False):
	data = {}
	data['id'] = r.id
	data['name'] = r.name
	data['description'] = r.description
	if detail_mode:
		data['timetable'] = [ TimeSpanSerializer(t) for t in r.timetable.all() ]
	return data

def SessionSerializer(s):
	data = {}
	data['session_id'] = str(s.session_hash)
	data['user'] = s.user.id
	return data

def TimeSpanSerializer(t):
	data = {}
	data['owner'] = RoomTimetable.objects.get(timespan=t).owner.id
	data['time_start'] = str(t.time_start)
	data['time_end'] = str(t.time_end)
	return data

def ParkSpotSerializer(p):
	data = {}
	data['id'] = p.id
	data['location'] = p.location
	data['spot'] = "free" if p.free else "taken"
	return data

def FoodTicketSerializer(t, detail_mode=False):
	data = {}
	data['id'] = t.id
	data['name'] = t.name
	data['thumb'] = t.thumb
	if detail_mode:
		data['description'] = t.description
		data['code'] = t.code
	return data

def GroupSerializer(g, detail_mode=False):
	data = {}
	data['id'] = g.id
	if detail_mode:
		membership = GroupMembership.objects.filter(group=g)
		data['members'] = [ { 'role': member.role.id, 'user': member.user.id } for member in membership ]
	else:
		data['members'] = [ u.id for u in g.members.all() ]
	return data