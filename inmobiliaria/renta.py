from inmobiliaria.models import *
from django.db.models import Q

def start_linear_rent(place_id):
	pass

def start_room_rent(room_id):
	pass

def get_all_room_concurrency(begin, end):
	query = (Q(fecha_inicio__lte = end) & Q(fecha_inicio__gte = begin)) | (Q(fecha_final__lte = end) & Q(fecha_final__gte = begin)) | (Q(fecha_inicio__lte = begin) & Q(fecha_final__gte = end))
	availables = list(Disponibilidad_de_cuarto.objects.filter(query))
	for available in availables:
		if available.fecha_inicio < begin:
			available.fecha_inicio = begin
		if available.fecha_final > end:
			available.fecha_final = end
	return availables

def get_room_concurrency(room_id, begin, end):
	room = Cuarto.objects.get(id = room_id)
	query = (Q(fecha_inicio__lte = end) & Q(fecha_inicio__gte = begin)) | (Q(fecha_final__lte = end) & Q(fecha_final__gte = begin)) | (Q(fecha_inicio__lte = begin) & Q(fecha_final__gte = end))
	availables = list(Disponibilidad_de_cuarto.objects.filter(cuarto__id = room_id).filter(query))
	print(availables)
	print(begin)
	print(end)
	for available in availables:
		if available.fecha_inicio < begin:
			available.fecha_inicio = begin
		if available.fecha_final > end:
			available.fecha_final = end
	print(availables)
	return availables

def get_all_place_concurrency(begin, end):
	query = (Q(fecha_inicio__lte = end) & Q(fecha_inicio__gte = begin)) | (Q(fecha_final__lte = end) & Q(fecha_final__gte = begin)) | (Q(fecha_inicio__lte = begin) & Q(fecha_final__gte = end))
	availables = list(Alquiler.objects.filter(query))
	for available in availables:
		if available.fecha_inicio < begin:
			available.fecha_inicio = begin
		if available.fecha_final > end:
			available.fecha_final = end
	return availables

def get_place_concurrency(place_id, begin, end):
	place = Lugar.objects.get(id = place_id)
	availables = list()
	if place.venta_o_renta == 'Renta de cuartos':
		query = (Q(fecha_inicio__lte = end) & Q(fecha_inicio__gte = begin)) | (Q(fecha_final__lte = end) & Q(fecha_final__gte = begin)) | (Q(fecha_inicio__lte = begin) & Q(fecha_final__gte = end))
		availables = list(Disponibilidad_de_cuarto.objects.filter(cuarto__casa__id = place_id).filter(query))
	else:
		query = (Q(fecha_inicio__lte = end) & Q(fecha_inicio__gte = begin)) | (Q(fecha_final__lte = end) & Q(fecha_final__gte = begin)) | (Q(fecha_inicio__lte = begin) & Q(fecha_final__gte = end))
		availables = list(Alquiler.objects.filter(casa__id = place_id).filter(query))
	for available in availables:
		if available.fecha_inicio < begin:
			available.fecha_inicio = begin
		if available.fecha_final > end:
			available.fecha_final = end
	return availables