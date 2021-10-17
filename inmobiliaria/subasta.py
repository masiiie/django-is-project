from .models import *
import datetime as dt
from inmobiliaria.pubflux import *

def start(id_place, time):
    """ 
    Deprecated
    Inicializa la subasta de la propiedad especificada.

    id_place: Propiedad en subasta
    time: Plazo máximo de subasta
    """ 
    try:
        place = Lugar.objects.get(id = id_place)
        if place and place.subastable:
            place.precio_de_subasta = place.precio_de_venta
            place.tiempo_restante = time
            place.save()
    except:
        return False

def update_all():
    """ 
    Deprecated
    Actualiza todas las propiedades en subasta y chequea si ya se llegó al plazo de alguna.
    """ 
    today = dt.date.today()
    q = Lugar.objects.filter(subastable = True,disponible = True)
    for place in q:
        if place.último_cambio < today:
            if place.tiempo_restante > 1:
                pass
            else:
                place.tiempo_restante -= 1
                place.último_cambio = today
                place.save()
    pass    

def place_bet(id_user,id_place,amount_rise):
    """ 
    Crea una nueva entrada de 'puja' en la tabla y actualiza la informacion correspondiente en la tabla
    'Lugar'.

    id_user: id del usuario que realizó la puja.
    id_place: lugar en subasta al que se le realizó la puja.
    amount_rise: cantidad pujada.
    """ 
    if amount_rise > 0: 
        place = Lugar.objects.get(id = id_place)
        place.precio_de_subasta = amount_rise
        user = User.objects.get(id = id_user)
        puja_actual = Puja.objects.create(lugar = place, usuario = user, tamanno_de_puja = amount_rise)
        print(puja_actual)
        puja_actual.save()
        place.save()

def bail_out(id_user,id_place):
    """ 
    Retira al usuario especificado de la subasta.

    id_user: Usuario a retirar.
    id_place: Lugar de subasta.
    """ 
    user = User.objects.get(id = id_user)
    place = Lugar.objects.get(id = id_place)
    qs = Puja.objects.filter(usuario = user,lugar = place).delete()

def end_auction(id_place):
    user_id = get_winner(id_place)
    if user_id:
        create_nego_solicitude(id_place,User.objects.get(id = user_id))
        return True
    else:
        return False

def get_winner(id_place):
    """ 
    Selecciona al usuario ganador de la subasta y lo retira de la misma en caso de que se necesite
    el segundo ganador.

    id_place: Lugar de subasta.
    """
    q = Puja.objects.filter(lugar__id = id_place)
    if q:
        place = Lugar.objects.get(id = id_place,disponible = True)
        latest = q.latest('tiempo')
        winner = latest.usuario.id
        place.precio_de_subasta = latest.tamanno_de_puja
        bail_out(winner,id_place)
        return winner
    return False