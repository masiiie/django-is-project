from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test,permission_required
from django.http.response import HttpResponseRedirect
from django.http import HttpResponse,JsonResponse
from administracion.models import PageImage
from inmobiliaria.models import *
from django.db.models import Q
from inmobiliaria.loadPhoto import *
from inmobiliaria.forms import *
from inmobiliaria.pubflux import *
from django.views.decorators.csrf import csrf_exempt
from inmobiliaria.manager import *
import random
import inmobiliaria.subasta as sub
import inmobiliaria.renta as rent
import json
import datetime
from django.core.serializers import serialize

def check_group(user,group_name):
	if user.is_authenticated:
		if not user.groups.filter(name = group_name) and not user.is_superuser:
			return False
	return True

@permission_required('inmobiliaria.view_data',login_url = '/')
def gerencia(request):
	return render(request,'inmobiliaria/gerencia.html',{'gerente':True})

@permission_required('inmobiliaria.view_data',login_url = '/')
@csrf_exempt
def datos(request):	
	if request.method == 'POST':
		if request.POST['modo_gerente'] =='true':
			nombres,dic = adminis_names()
			result = []
			if request.POST['opcion_gerente'] == 'alquileres gestionados':
				result = adminis_alquileres(dic)
			else:
				result = adminis_venta(dic)	

			print('names '+str(nombres))
			print('result '+str(result))	
			data={'datasets': [{'label':request.POST['opcion_gerente'],'fill':True,'backgroundColor':'rgb(%s,%s,%s)'%(random.randint(0,255),random.randint(0,255),random.randint(0,255)),'data':result}],
			'labels':nombres}
			return JsonResponse(data)

		result = info_handler(request.POST)
		dict_name={'T':'Total','V':'Ventas',0:'Ventas','S':'Subastas',1:'Subastas','A':'Alquileres',2:'Alquileres'}
		if request.POST['info'] == 'TT':
			data={'datasets': []}
			for index in range(len(result)):
				dataset = result[index]
				data['datasets']+=[{'label':dict_name[index],'fill':True,'backgroundColor':'rgb(%s,%s,%s)'%(random.randint(0,255),random.randint(0,255),random.randint(0,255)),'data':dataset}]
		else:
			data={'datasets': [{'label':dict_name[request.POST['info']],'fill':True,'backgroundColor':'rgb(%s,%s,%s)'%(random.randint(0,255),random.randint(0,255),random.randint(0,255)),'data':result}]}
		return JsonResponse(data)
	return JsonResponse({})
	# return render(request,'inmobiliaria/gerencia.html',{'gerente':True})

def index(request):
	
	''' consultas para rellenar la pagina
	sacar estas consultas de aqui y que se hagan una sola vez
	no es necesario hacerlas cada vez que se entre a la pagina al final esta 
	informacion no cambia tanto '''
   
	casas = Lugar.objects.filter(disponible = True,chequeado = True)
	Cant_casas =len(Lugar.objects.filter(disponible = True,chequeado = True))
	casa_ciu_camp_pl_per=[]
	if Cant_casas!=0:
		casa_ciu_camp_pl_per=[
			[int((len(Lugar.objects.filter(ubicacion='CI'))/Cant_casas)*100),'En la Ciudad'],
			[int((len(Lugar.objects.filter(ubicacion='CP'))/Cant_casas)*100),'En el Campo'],
			[int((len(Lugar.objects.filter(ubicacion='PL'))/Cant_casas)*100),'En la Playa'],
			[int((len(Lugar.objects.filter(ubicacion='PE'))/Cant_casas)*100),'En la Periferia'],
			]
	casas = casas.order_by('-evaluacion')[:6]

	return render(request,'inmobiliaria/index.html',{'img':load(),'stats':casa_ciu_camp_pl_per,'top':casas})

def calendar(request,place_id):
	return render(request,'inmobiliaria/calendario.html')

def alquiler(request):
	query=Q(venta_o_renta='Renta linear') | Q(venta_o_renta='Renta de cuartos')
	alquileres =Lugar.objects.filter(query)
	return render(request,'inmobiliaria/alquiler_venta.html',{'tipo':'Alquiler','casas':alquileres,'img':load()})

def venta(request):
	ventas = Lugar.objects.filter(venta_o_renta = 'Venta',chequeado = True, disponible = True)
	return render(request,'inmobiliaria/alquiler_venta.html',{'tipo':'Venta','casas':ventas,'img':load()})

def mapa(request):
	return render(request,'inmobiliaria/mapa.html',{})

def casa_en_venta(request):
	form = SolicitudForm()
	form.fields['venta_o_renta'] = 'Venta' 
	return render(request,'inmobiliaria/insertar.html',{'form':form,'thing': 'Solicitud'})

def casa_en_alquiler(request):
	return render(request,'inmobiliaria/casa.html',{})

@login_required(login_url = '/')
def solicitud(request,typ):
	if request.method == 'POST':
		create_solicitude(request.POST)
		return HttpResponseRedirect('/profile/client/pubs/all')
	if typ == 'sell':
		form = SolicitudForm(initial = {'venta_o_renta':'Venta', 'usuario':request.user})
	if typ == 'rent':
		form = SolicitudForm(initial = {'venta_o_renta':'Renta linear', 'usuario':request.user})

	form.fields['usuario'].queryset = User.objects.filter(id = request.user.id)        
	return render(request,'inmobiliaria/insertar.html',{'form':form,'solicitude':True})

@login_required(login_url = '/')
def crear_perfil(request):
	if request.method == 'POST':
		user = User.objects.get(id = request.user.id)
		user.email = request.POST['email']
		user.first_name = request.POST['first_name']
		user.last_name = request.POST['last_name']
		new_group = Group.objects.get(name = 'Cliente')
		user.groups.add(new_group)
		user.save()
		return HttpResponseRedirect('/profile/client/pubs/all')

	form = ClientUserForm()
	return render(request,'inmobiliaria/insertar.html',{'form':form, 'thing':'Perfil','formb':True})

@login_required(login_url = '/')
def proponer_venta(request):
	if request.user.has_perm('inmobiliaria.view_profile'):
		return HttpResponseRedirect('/profile/solicite/sell')
	return HttpResponseRedirect('/profiles/new_profile')

@login_required(login_url = '/')
def proponer_alquiler(request):
	if request.user.has_perm('inmobiliaria.view_profile'):
		return HttpResponseRedirect('/profile/solicite/rent')
	return HttpResponseRedirect('/profiles/new_profile')

@login_required(login_url = '/')
def solicita_accion_casa(request,typ,place_id):
	if typ == 'buy':
		#hacer aqui la venta
		pass
	if typ == 'rent':
		#hacer aqui la renta
		pass
	if typ == 'auction':
		#hacer aqui subasta
		if request.user.has_perm('inmobiliaria.view_profile'):
			pass
		else:
			return HttpResponseRedirect('/profiles/new_profile')
		pass
	pass

@login_required(login_url = '/')
def renta_cuarto(request,place_id,room_id):
	pass

@permission_required('inmobiliaria.view_profile',login_url = '/')
def ver_perfil(request, typ, option):
	"""
	Muestra la información relevante para el usuario en cuestión.
	"""
	negs = False    
	if typ == 'perit':
		casas = Lugar.objects.filter(perito = request.user).filter(disponible = True)
		pubs = Solicitud.objects.filter(perito = request.user)
	if typ == 'client':
		casas = Lugar.objects.filter(propietario = request.user).filter(disponible = True)
		pubs = Solicitud.objects.filter(usuario = request.user)
		query=Q(solicitante=request.user) | Q(lugar__propietario=request.user)       
		negs = SolicitudDeNegociacion.objects.filter(query)
	if typ == 'agent':
		casas = Lugar.objects.filter(agente = request.user).filter(disponible = True)
		pubs = Solicitud.objects.all()
		negs = SolicitudDeNegociacion.objects.filter(lugar__agente = request.user)

	opt = 'validadas o pendientes'
	if option == 'published':
		opt = 'validadas'
		pubs.filter(chequeado = True)

	if option == 'pending':
		opt = 'pendientes'
		pubs.filter(chequeado = False)
	print(pubs)
	
	return render(request,'inmobiliaria/perfil.html',{'pubs':pubs, 'option':opt,'casas':casas,'negociations':negs})

def recorrido(request,id_perito):
    
	return render(request,'inmobiliaria/recorrido.html')

def recorrido_json(request,id_perito):
    
	pubs = Solicitud.objects.filter(perito = id_perito)

	print(pubs)
	json =serialize('json',pubs,fields=['nombre','lat','lng'])
	return HttpResponse(json,content_type='application/json')

@permission_required('inmobiliaria.add_lugar')
def valida_solicitud(request,sol_id):
	sol = Solicitud.objects.get(id = sol_id)
	if request.method == 'POST':
		if request.POST['accion'] == 'assign':
			try:
				sol.perito = User.objects.get(id = request.POST['peritos'])
				sol.chequeado = True
				sol.save()
			except:
				pass
		if request.POST['accion'] == 'validate':
			return HttpResponseRedirect('/staff/insert_place/%d/%d' %(int(sol_id),int(sol.usuario.id)))

		if request.POST['accion'] == 'delete':
			Solicitud.objects.get(id = sol_id).delete()
	peritos = []
	print(request.user.get_group_permissions())
	grp = Group.objects.get(name = "Perito")
	for user in User.objects.all():
		if grp in user.groups.all():
			peritos.append(user)
	return render(request,'inmobiliaria/valida_solicitud.html',{'sol': sol,'peritos':peritos})

@permission_required('inmobiliaria.add_lugar')
def ver_solicitudes(request,option):
	if option == 'all':
		opt = 'pendientes o validadas'
		pubs = Solicitud.objects.all()

	if option == 'published':
		opt = 'validadas'
		pubs = Solicitud.objects.filter(casa__chequeado = True, disponible = True)

	if option == 'pending':
		opt = 'pendientes'
		query = Q(casa = null ) | Q(casa__chequeado = False)
		pubs = Solicitud.objects.filter(query)
	return render(request,'inmobiliaria/solicitudes.html',{'pubs':pubs , 'option':opt})

@permission_required('inmobiliaria.add_lugar',raise_exception = True)
def empleo(request):
	return render(request,'inmobiliaria/staff.html',)

@permission_required(['inmobiliaria.add_lugar','inmobiliaria.change_lugar','inmobiliaria.delete_lugar','inmobiliaria.add_cuarto','inmobiliaria.change_cuarto','inmobiliaria.delete_cuarto'],raise_exception = True)
def publicaciones(request,option):
	if option == 'pending':
		pendingforms = Lugar.objects.filter(chequeado = False,disponible = True)
		option = 'pendientes'
	elif option == 'published':
		pendingforms = Lugar.objects.filter(chequeado = True,disponible = True)
		option = 'validados'
	elif option == 'all':
		pendingforms = Lugar.objects.all()
		option = 'pendientes o validados'
	grp = Group.objects.get(name = "Perito")
	if grp in request.user.groups.all():
		pubs = Solicitud.objects.filter(perito = request.user)
	else:
		pubs = Solicitud.objects.filter(chequeado = False)
	return render(request,'inmobiliaria/vista_publicaciones.html',{'casas':pendingforms,'option':option,'pubs':pubs})

@permission_required(['inmobiliaria.add_lugar','inmobiliaria.add_cuarto'],raise_exception = True)
def insertar_lugar(request,sol_id = False,prop_id = False):
	if request.method == 'POST':
		if create_place(request.POST,request.FILES):
			if request.POST['venta_o_renta'] == 'Renta de cuartos':
				return HttpResponseRedirect('/staff/insert_room/%d' % Lugar.objects.get(calle_principal = request.POST['calle_principal'],numero_de_vivienda = request.POST['numero_de_vivienda']).id)
			return HttpResponseRedirect('/profile/perit/pubs/all')

	if sol_id:
		sol = Solicitud.objects.get(id = sol_id)
		form = LugarForm(initial = {'nombre':sol.nombre_de_publicacion,
									'calle_principal':sol.calle_principal,
									'calle_secundaria':sol.calle_secundaria,
									'calle_secundaria_opcional':sol.calle_secundaria_opcional,
									'tiene_calle_secundaria_opcional':sol.tiene_calle_secundaria_opcional,
									'numero_de_vivienda':sol.numero_de_vivienda,
									'municipio':sol.municipio,
									'provincia':sol.provincia,
									'solicitud':sol,
									'perito':request.user.id,
									'propietario':sol.usuario,
									'venta_o_renta':sol.venta_o_renta,})

		form.fields['solicitud'].queryset = Solicitud.objects.filter(id = sol_id)
		form.fields['propietario'].queryset = User.objects.filter(id = prop_id)
		form.fields['perito'].queryset = User.objects.filter(id = request.user.id)
	else:
		form = LugarForm()
		form.fields['solicitud'].queryset = Solicitud.objects.filter(perito__id = request.user.id)
		form.fields['propietario'].queryset = User.objects.filter(groups__name = 'Cliente')
		form.fields['perito'].queryset = User.objects.filter(groups__name = 'Perito')

	form.fields['agente'].queryset = User.objects.filter(groups__name = 'Administrador')
	form.fields['tags'].queryset = Tag.objects.filter(tipo = 'CA')
	return render(request,'inmobiliaria/insertar.html',{'form':form, 'thing':'Inmueble','inserting_place': True})

@permission_required(['inmobiliaria.add_lugar','inmobiliaria.add_cuarto'],raise_exception = True)
def insertar_cuarto(request,place_id = False):
	if request.method == 'POST':
		create_room(request.POST)
	if place_id:
		place = Lugar.objects.get(id = place_id)
		form = CuartoForm(initial = {'casa':place,})
		if place.cantidad_de_cuartos - len(Cuarto.objects.filter(casa = place)) > 0 and place.venta_o_renta == 'Renta de cuartos':
			return render(request,'inmobiliaria/insertar.html',{'form':form})
		else:
			return HttpResponseRedirect('/')
	form = CuartoForm()
	form.fields['casa'].queryset = Lugar.objects.filter(venta_o_renta = 'Renta de cuartos')
	return render(request,'inmobiliaria/insertar.html',{'form':form,'thing':'Habitación'})

@permission_required(['inmobiliaria.add_lugar','inmobiliaria.add_cuarto'],raise_exception = True)
def insertar_trabajador(request):
	message = ''
	if request.method == 'POST':
		if User.objects.filter(username = request.POST['username']):
			message = 'El nombre de usuario ya está en uso'
		else:
			new_user = User.objects.create_user(
											username = request.POST['username'],
											first_name = request.POST['first_name'],
											last_name = request.POST['last_name'],
											email = request.POST['email'],
											password = request.POST['password'])
			new_user.groups = request.POST['groups']
			new_user.save()
			return HttpResponseRedirect('/profile/agent/pubs/all')
	form = StaffUserForm()
	return render(request,'inmobiliaria/insertar.html',{'form':form, 'thing':'Trabajador','message':message})

@permission_required(['inmobiliaria.add_lugar','inmobiliaria.add_cuarto'],raise_exception = True)
def insertar_tag(request,typ = False):
	if request.method == 'POST':
		create_tag(request.POST)
	form = TagForm()
	# if tipe == "place":
	#     form.fields['tipo'].choices = ("CA","Tag de Casa")
	# if tipe == "room":
	#     form.fields['tipo'].choices = ("CU","Tag de Casa")
	return render(request,'inmobiliaria/insertar.html',{'form':form, 'thing':'Tag','inserting_tag_casa': True})

@permission_required(['inmobiliaria.change_lugar',],raise_exception = True)
def valida_neg_solicitud(request,sol_id):
	if request.method == 'POST':
		if request.POST['accion'] == 0:
			act_date = datetime.date.today()
			validate_buy_solicitude(request.user,sol_id,request.POST['date'])
		if request.POST['accion'] == 2:
			sol = SolicitudDeNegociacion.objects.get(id = sol_id)
			place = sol.lugar
			sol.delete()
			if not sub.end_auction(place.id):
				place.disponible = False
				place.save()
		else:
			sol = SolicitudDeNegociacion.objects.get(id = sol_id)
			place = sol.lugar
			place.disponible = False
			Log.objects.create(usuario = sol.solicitante, nombre = place, accion = 'CM')
			SolicitudDeNegociacion.objects.filter(lugar = place).delete()
			place.save()
		return HttpResponseRedirect('/profile/agent/pubs/all')


	sol = SolicitudDeNegociacion.objects.get(id = sol_id)
	return render(request,'inmobiliaria/valida_neg_solicitud.html',{'sol': sol})

def vista_cuarto(request,place_id,room_id):
	"""
	Muestra los datos individuales de un cuarto así como los cuartos relacionados
	e información del lugar que los contiene.
	"""
	if request.user.has_perms(['inmobiliaria.add_lugar','inmobiliaria.change_lugar']):
		typ = 'agent'
	elif request.user.has_perms(['inmobiliaria.add_lugar']):
		typ = 'perit'
	else:
		typ = 'client'

	if request.method == 'POST':
		if 'accion' in request.POST.keys() and request.POST['accion'] == 'validate':
			validate_place(place_id)
			return HttpResponseRedirect('/profile/%s/pubs/all' %typ)
		elif 'accion' in request.POST.keys() and request.POST['accion'] == 'delete':
			delete_place(place_id)
			return HttpResponseRedirect('/pubs/places/all')

	pendingplace = Lugar.objects.get(id = room_id)
	rooms = Cuarto.objects.filter(casa = place_id)
	return render(request,'inmobiliaria/vista_cuarto.html',{'cuarto':pendingplace,'rooms':rooms,'roomform':roomform,'ubicacion':ubication[pendingplace.ubicacion],})
def vista_casa(request,place_id):
	"""
	Muestra información individual del lugar en cuestión y si este propone renta de cuartos
	entonces muestra información acerca de los mismos.
	"""
	if request.user.has_perms(['inmobiliaria.add_lugar','inmobiliaria.change_lugar']):
		typ = 'agent'
	elif request.user.has_perms(['inmobiliaria.add_lugar']):
		typ = 'perit'
	else:
		typ = 'client'

	if request.method == 'POST' and 'accion' in request.POST.keys():
		if request.POST['accion'] == 'validate':
			validate_place(place_id)
			return HttpResponseRedirect('/profile/%s/pubs/all' %typ)
		if request.POST['accion'] == 'delete':
			delete_place(place_id)
			return HttpResponseRedirect('/profile/%s/pubs/all' %typ)
		if request.POST['accion'] == 'edit':
			return HttpResponseRedirect('/profile/%s/pubs/all' %typ)
		if request.POST['accion'] == 'buy':
			if not request.user.has_perm('inmobiliaria.view_profile'):
				return HttpResponseRedirect('/profiles/new_profile')
			create_nego_solicitude(place_id,request.user,'Compra')
			return HttpResponseRedirect('/profile/%s/pubs/all' %typ)
		if request.POST['accion'] == 'rent':
			return HttpResponseRedirect('/scheduler/%s' %place_id)
		if request.POST['accion'] == 'auction':
			return HttpResponseRedirect('/pubs/places/%d/action/auction' %place_id)

	pendingplace = Lugar.objects.get(id = place_id)
	auction = True if pendingplace.subastable else False
	rooms = Cuarto.objects.filter(casa = pendingplace)
	roomform = CuartoForm()
	return render(request,'inmobiliaria/vista_casa.html',{'casa':pendingplace,'rooms':rooms,'roomform':roomform,'ubicacion':ubication[pendingplace.ubicacion],'auction':auction})
def entrar(request):
	if request.method == 'POST':
		# if request.POST.has_key('user') and request.POST.has_key('pass'):
		user = authenticate(username=request.POST['user'], password=request.POST['pass'])
		if user is not None:
			login(request, user)
			# messages.add_message(request, messages.INFO, "Bienvenido " + user.username)
		   
		# else:
		#     messages.add_message(request, messages.ERROR,"Credenciales incorrectas")

	return HttpResponseRedirect('/')
def register(request):
	if request.method == 'POST':
		if request.POST["pass"] == request.POST["pass2"]:
			user = User.objects.create_user(username=request.POST['user'], password=request.POST['pass'])
			if user is not None:
				print('aqui')
				login(request, user)
				return HttpResponseRedirect('/')
		else:
			return render(request,'inmobiliaria/register.html',{'message':'Las contraseñas no coinciden'})            
	return render(request,'inmobiliaria/register.html',)  
def salir(request):
	logout(request)
	return HttpResponseRedirect('/')
@csrf_exempt
def pujar(request):
	place = Lugar.objects.get(id = request.POST['id'])
	a = int(request.POST['price'])
	sub.place_bet(request.user.id,place.id,a)
	return HttpResponseRedirect('/pubs/places/%d' %place.id)

@csrf_exempt
def getTime(request):
	if request.method == 'POST':
		place = Lugar.objects.get(id = request.POST['id'])
		previous = Puja.objects.filter(lugar = place).order_by('tiempo')[:5]
		resp = []
		for i in previous:
			print(i)
			resp += [{'name':i.usuario.username,'price':i.tamanno_de_puja}]
		pub_date = place.ultimo_cambio
		end_date = place.fecha_finalizacion

		if pub_date - end_date <= datetime.timedelta(0):
			if not sub.end_auction(place.id):
				place.disponible = False
				place.save()
				return JsonResponse({'url':'/'})

		return JsonResponse({'begin':pub_date,'end':end_date,'previousActions':resp})
	return ()

def calendarJSON(request,start,end,place_id):
	start = start.split('-')
	i_dia =int(start[2]) if not start[2][0] == '0' else int(start[2][1])
	i_mes = int(start[1]) if not start[1][0] == '0' else int(start[1][1])
	i_anno = int(start[0])
	fecha_ini = datetime.date(i_anno,i_mes,i_dia)
	
	end = end.split('-')
	f_dia =int(end[2]) if not end[2][0] == '0' else int(end[2][1])
	f_mes = int(end[1]) if not end[1][0] == '0' else int(end[1][1])
	f_anno = int(end[0])
	fecha_fin = datetime.date(f_anno,f_mes,f_dia)

	value = []
	q = []
	place = Lugar.objects.get(id = place_id)
	if place.venta_o_renta == 'Renta linear':
		q = rent.get_place_concurrency(place_id, fecha_ini, fecha_fin)
		for con in q:
			value += [{'title': con.cuarto.usuario,'start':con.fecha_inicio,'end':con.fecha_final}]
			
	if place.venta_o_renta == 'Renta de cuartos':
		rooms = Cuarto.objects.filter(casa = place)
		for room in rooms:
			color = 'rgb(%s,%s,%s)'%(random.randint(0,255),random.randint(0,255),random.randint(0,255))
			q = rent.get_room_concurrency(room.id,fecha_ini,fecha_fin)
			for con in q:
				value += [{'title': str(con.cuarto),'start':con.fecha_inicio,'end':con.fecha_final,'backgroundColor':color}]
    				
	#hay q ver como cambiar la parte izquierda del json que se va a generar cuando se haga la consulta
	#value = [{'title': 'All Day Event','start': '2018-05-01','end': '2018-05-05','url': 'http://google.com/'}]
	return JsonResponse(value,safe = False)

	
	return HttpResponseRedirect('/')
