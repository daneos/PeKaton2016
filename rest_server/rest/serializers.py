def RoomSerializer(r):
	data = {}
	data['id'] = r.id
	data['name'] = r.name
	data['description'] = r.description
	return data