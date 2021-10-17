from .models import *
from django.core.mail import send_mail
from django.core.files.storage import FileSystemStorage


def create_solicitude(request_dict):
    user = User.objects.get(id = request_dict['usuario'])
    tcso = True if 'tiene_calle_secundaria_opcional' in request_dict.keys() else False
    Solicitud.objects.create(
                            nombre_de_publicacion = request_dict['nombre_de_publicacion'],
                            usuario = user,
                            calle_principal=request_dict['calle_principal'],
                            calle_secundaria=request_dict['calle_secundaria'],
                            calle_secundaria_opcional=request_dict['calle_secundaria_opcional'],
                            tiene_calle_secundaria_opcional=tcso,
                            municipio=request_dict['municipio'],
                            provincia=request_dict['provincia'],
                            venta_o_renta=request_dict['venta_o_renta'],
                            lat = request_dict['lat'],
                            lng = request_dict['lng'])

def create_place(request_dict,files):
    """
    Crea una entrada de un lugar no validado en la base de datos así como un formulario de validacion
    para el mismo dirigido al agente asignado a la localizacion.
    """
    if Lugar.objects.filter(calle_principal = request_dict['calle_principal'],
                            calle_secundaria = request_dict['calle_secundaria'],
                            numero_de_vivienda = request_dict['numero_de_vivienda'],
                            provincia = request_dict['provincia'],
                            municipio = request_dict['municipio'],
                            ):
        raise Exception("El lugar ya está registrado")

    sub = True if 'subastable' in request_dict.keys() else False
    tcso = True if 'tiene_calle_secundaria_opcional' in request_dict.keys() else False
    per = User.objects.get(id = request_dict['perito'])
    prop = User.objects.get(id = request_dict['propietario'])
    agent = User.objects.get(id = request_dict['agente'])
    place = Lugar.objects.create(
                                nombre = request_dict['nombre'],
                                perito=per,
                                agente=agent,
                                calle_principal=request_dict['calle_principal'],
                                calle_secundaria=request_dict['calle_secundaria'],
                                calle_secundaria_opcional=request_dict['calle_secundaria_opcional'],
                                ubicacion=request_dict['ubicacion'],
                                propietario=prop,
                                descripcion=request_dict['descripcion'],
                                foto1=files['foto1'],
                                foto2=files['foto2'],
                                foto3=files['foto3'],
                                cantidad_de_bannos=request_dict['cantidad_de_bannos'],
                                cantidad_de_cuartos=request_dict['cantidad_de_cuartos'],
                                cantidad_de_plantas=request_dict['cantidad_de_plantas'],
                                numero_de_vivienda=request_dict['numero_de_vivienda'],
                                precio_de_alquiler=request_dict['precio_de_alquiler'],
                                precio_de_venta=request_dict['precio_de_venta'],
                                fecha_finalizacion=request_dict['fecha_finalizacion'],
                                tiene_calle_secundaria_opcional=tcso,
                                municipio=request_dict['municipio'],
                                provincia=request_dict['provincia'],
                                venta_o_renta=request_dict['venta_o_renta'],
                                subastable=sub,
                                lat = request_dict['lat'],
                                lng = request_dict['lng'],                                
                                )
    foto= files['foto1']
    fs = FileSystemStorage()
    fs.save(foto.name, foto) 
    
    foto= files['foto2']
    fs.save(foto.name, foto)
    
    foto= files['foto3']
    fs.save(foto.name, foto)
    
    place.tags = request_dict.getlist('tags')
    place.save()
    Solicitud.objects.get(id = request_dict['solicitud']).delete()
    return True

def create_room(request_dict):
    """
    Crea una entrada de una habitación no validada en la base de datos así como un formulario de validación
    para la misma derigido al agente asignado a la localizacion.
    """
    place = Lugar.objects.get(id = request_dict['casa'])
    if len(Cuarto.objects.filter(casa = place)) >= place.cantidad_de_cuartos:
        raise Exception("Todas la habitaciones del lugar estan publicadas")

    bc = True if 'banno_compartido' in request_dict.keys() else False
    room = Cuarto.objects.create(casa = place,
                                cantidad_de_camas = request_dict['cantidad_de_camas'],
                                banno_compartido = bc,
                                )
    
    room.tags = request_dict.getlist('tags')
    room.save()
    return True

def create_tag(request_dict):
    tag = Tag.objects.create(nombre = request_dict['nombre'],
                            tipo = request_dict['tipo']
                            )
    tag.save()
    return True

def deep_delete_place():
    pass

def delete_place(place_id):
    try:
        Lugar.objects.filter(id = place_id).delete()

    except:
        raise Exception('Lugar especificado no existe')
    return True

def delete_room(room_id):
    Cuarto.objects.get(id = room_id).delete()

def validate_place(place_id):
    place = Lugar.objects.get(id = place_id)
    place.chequeado = True
    place.save()
    return True

def create_nego_solicitude(place_id,user,typ,room_id = False):
    place = Lugar.objects.get(id = place_id)
    if room_id:
        room = Cuarto.objects.get(id = room_id)
        q = SolicitudDeNegociacion.objects.create(lugar = place,solicitante = user, cuarto = room_id, tipo = typ)
    else:
        q = SolicitudDeNegociacion.objects.create(lugar = place,solicitante = user, tipo = typ)
    return q

def validate_buy_solicitude(user,sol_id,fecha):
    sol = SolicitudDeNegociacion.objects.get(id = sol_id)
    sol.estado = "Cita Programada"
    sol.fecha = fecha
    sol.save()
    # send_mail(
    #         'Cita para compra de inmueble %s' %(str(sol.lugar)),
    #         'Buenos dias, se ha programado una cita para realizar la compra del' + \
    #         'inmueble %s para la fecha %s, asista a nuestras oficinas por favor. Muchas gracias' %(str(sol.lugar),str(sol.fecha)),
    #         str(user.email),
    #         [str(sol.solicitante.email),str(sol.lugar.propietario.email)],)
    return sol
