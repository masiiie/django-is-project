from django.conf.urls import url,include
from .views import *

urlpatterns = [
    url(r'^$',index, name='index'),
    url(r'^pubs/rents$',alquiler, name='alquiler'),
    url(r'^pubs/sells$',venta, name='venta'),
    url(r'^casaventa$',casa_en_venta, name='casa_venta'),
    url(r'^casaalquiler$',casa_en_alquiler, name='casa_alquiler'),
    url(r'^gestventa$',proponer_venta, name='vender'),
    url(r'^gestalquiler$',proponer_alquiler, name='alquilar'),

    url(r'^getTime$',getTime),
    url(r'^realizarPuja$',pujar),  
    url(r'^scheduler/(?P<place_id>\d+)$',calendar),
    url(r'^dateintersection/(\d+-\d+-\d+)/(\d+-\d+-\d+)/(\d+)$',calendarJSON),

    url(r'^profile/(?P<typ>(agent|perit|client))/pubs/(?P<option>(all|published|pending))$',ver_perfil, name='ver_perfil'),
    url(r'^profile/solicite/(?P<typ>(rent|sell))$',solicitud, name='solicitud'),
    url(r'^profiles/new_profile$',crear_perfil, name='crear_perfil'),
    url(r'^recorrido/(?P<id_perito>\d+)/$',recorrido, name='recorrido'),
    url(r'^recorridojson/(?P<id_perito>\d+)/$',recorrido_json, name='recorridojson'),
    

    # url(r'^staff/insert_user$',insertar_usuario, name='insert_user'),
    url(r'^management$',gerencia, name='gerencia'),
    url(r'^graph$',datos, name='datos'),
    url(r'^staff$',empleo, name='empleo'),
    url(r'^staff/insert_member$',insertar_trabajador, name='empleo'),
    url(r'^staff/insert_place$',insertar_lugar, name='insert_place'),
    url(r'^staff/insert_place/(?P<sol_id>\d+)/(?P<prop_id>\d+)$',insertar_lugar, name='insert_place_sol'),
    url(r'^staff/insert_room$',insertar_cuarto, name='insert_room'),
    url(r'^staff/insert_room/(?P<place_id>\d+)$',insertar_cuarto, name='insert_room'),
    url(r'^staff/insert_tag/(?P<typ>(place|room|any))$',insertar_tag, name='insert_tag'),
    url(r'^staff/solicitudes/(?P<option>(pending|checked|all))$',ver_solicitudes, name='ver_solicitudes'),
    url(r'^staff/solicitudes/validate/(?P<sol_id>\d+)$',valida_solicitud, name='valida_solicitud'),
    url(r'^staff/solicitudes/bussiness/validate/(?P<sol_id>\d+)$',valida_neg_solicitud, name='valida_neg_solicitud'),    

    url(r'^pubs/places/(?P<option>(pending|published|all))$',publicaciones, name='publicaciones'),
    url(r'^pubs/places/(?P<place_id>\d+)/room/(?P<room_id>\d+)$',vista_cuarto, name='publicaciones'),    
    url(r'^pubs/places/(?P<place_id>\d+)$',vista_casa, name='validar'),
    url(r'^pubs/places/(?P<place_id>\d+)/room/(?P<room_id>\d+)/solicite/rent$',renta_cuarto, name='publicaciones'),    
    url(r'^pubs/places/(?P<place_id>\d+)/action/(?P<typ>(rent|buy|auction))$',solicita_accion_casa, name='validar'),

    url(r'^register$', register , name='register'),    
    url(r'^login$', entrar , name='login'),
    url(r'^logout$', salir , name='logout'),
]
