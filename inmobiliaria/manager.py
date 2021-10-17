from datetime import *
from inmobiliaria.models import *
from django.db.models import Q
from inmobiliaria.renta import *
import calendar

def adminis_names():
	i = 0
	dic = {}
	administ_nombres = []
	grp = Group.objects.get(name = "Administrador")

	for user in User.objects.all():
		if grp in user.groups.all():
			dic[user.username]=i
			i+=1
			administ_nombres.append(user.username)

	return (administ_nombres,dic)


def adminis_venta(dic):
	ventas = [0]*len(dic)
	for x in Log.objects.all():
		ventas[dic[x.nombre.agente.username]]+=1
	return ventas

def adminis_alquileres(dic):
	alq = [0]*len(dic)
	for x in Alquiler.objects.all():
		alq[dic[x.casa.agente.username]]+=1
	return alq	



def info_handler(POST):
	year = int(POST['year'])
	month = int(POST['month'])
	mode = int(POST['mode'])
	typ = POST['type']
	local = POST['locale']
	info = POST['info']
	amount_days = 0

	if month != 0:
		amount_days = calendar.monthrange(year,month)[1]

	if typ == 'true':
		#publicaciones
		if mode == 1:
			#temporal
			if local == 'R':
				#cuartos
				pass
			if local == 'H':
				#lugares
				return get_pubs_info_temporal(year,month,amount_days,info)
		else:
			#acumulado
			if local == 'R':
				#cuartos
				pass
			if local == 'H':
				#lugares
				return get_pubs_info_acumulated(year,month,amount_days,info)
	else:
		#acciones
		if mode:
			#temporal
			return get_action_info_temporal(year, month, amount_days, local, info)
			
		else:
			#acumulado
			return get_action_info_acumulated(year, month, amount_days, local, info)

def get_pubs_info_temporal(year, month, amount_days, request_info):
	return _get_pubs_info(year,month,amount_days,request_info)

def get_pubs_info_acumulated(year, month, amount_days, request_info):
	response = _get_pubs_info(year,month,amount_days,request_info)
	for i in range(1,len(response)):
		response[i] += response[i-1]
	return response

def _get_pubs_info(year, month, amount_days, request_info):
	query = Q()
	if request_info == 'V':
		query = Q(venta_o_renta = 'Venta') & Q(subastable = False)
	if request_info == 'S':
		query = Q(venta_o_renta = 'Venta') & Q(subastable = True)
	if request_info == 'A':
		query = Q(venta_o_renta = 'Renta linear') | Q(venta_o_renta = 'Renta de cuartos')
	if request_info == 'TT':
		return [_get_pubs_info(year,month,amount_days,'V'),
				_get_pubs_info(year,month,amount_days,'S'),
				_get_pubs_info(year,month,amount_days,'A'),]
	else:
		if month != 0:
			response = [0]*amount_days
			for i in range(amount_days):
				objects = Lugar.objects.filter(query).filter(ultimo_cambio = date(year,month,i+1),disponible = True)
				response[i] = len(objects)
				print(objects)

		else:
			response = [0]*12
			for i in range(1,12):
				query_month = (Q(ultimo_cambio__gte = date(year,i,1)) & Q(ultimo_cambio__lt = date(year,i+1,1)))
				response[i-1] = len(Lugar.objects.filter(query).filter(query_month))
			query_month = (Q(ultimo_cambio__gte = date(year,12,1)) & Q(ultimo_cambio__lt = date(year + 1,1,1)))
			response[11] = len(Lugar.objects.filter(query).filter(query_month & Q(disponible = True)))
		return response

def get_action_info_temporal(year, month, amount_days, local, request_info):
	if local == 'H':
		if request_info=='A':
			return _get_place_rents_info(year,month,amount_days)
		if request_info=='V':
			return _get_sells_info(year,month,amount_days)
	else:
		if request_info=='A':
			return _get_room_rents_info(year,month,amount_days)

def get_action_info_acumulated(year, month, amount_days, local, request_info):
	response = [0]
	if local == 'H':
		if request_info=='A':
			response = _get_place_rents_info(year,month,amount_days)
		if request_info=='V':
			response = _get_sells_info(year,month,amount_days)
	else:
		if request_info=='A':
			response = _get_room_rents_info(year,month,amount_days)

	for i in range(1,len(response)):
		response[i] += response[i-1]
	return response

def _get_sells_info(year, month, amount_days):
	if month != 0:
		response = [0]*amount_days
		for i in range(amount_days):
			objects = Log.objects.filter(tiempo = date(year,month,i) , accion = 'CM',disponible = True)
			response[i] = len(objects)
	else:
		response = [0]*12
		for i in range(1,12):
			query = Q(tiempo__gte = date(year,i,1)) & Q(tiempo__lt = date(year,i+1,1))
			objects = Log.objects.filter(accion = 'CM',disponible = True).filter(query)
			response[i-1] = len(objects)
		query = Q(tiempo__gte = date(year,12,1)) & Q(tiempo__lt = date(year+1,1,1))
		objects = Log.objects.filter(accion = 'CM',disponible = True).filter(query)
		response[11] = len(objects)
	return response

def _get_room_rents_info(year, month, amount_days):
	query = Q()
	if month != 0:
		response = [0]*amount_days
		for i in range(1,amount_days):
			objects = get_all_room_concurrency(date(year,month,i),date(year,month,i+1))
			response[i] = len(objects)
	else:
		response = [0]*12
		for i in range(1,12):
			objects = get_all_room_concurrency(date(year,i,1),date(year,i+1,1) - timedelta(1))
			response[i-1] = len(objects)
		objects = get_all_room_concurrency(date(year,12,1),date(year+1,1,1) - timedelta(1))
		response[11] = len(objects)
	return response

def _get_place_rents_info(year, month, amount_days):
	query = Q()
	if month != 0:
		response = [0]*amount_days
		for i in range(1,amount_days+1):
			objects = get_all_place_concurrency(date(year,month,i),date(year,month,i+1))
			response[i-1] = len(objects)
	else:
		response = [0]*12
		for i in range(1,12):
			objects = get_all_place_concurrency(date(year,i,1),date(year,i+1,1) - timedelta(1))
			response[i-1] = len(objects)
		objects = get_all_place_concurrency(date(year,12,1),date(year + 1,1,1) - timedelta(1))
		response[11] = len(objects)
	return response
