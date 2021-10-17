# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.db.models import Q
from .db_connect import *
from django.core.serializers import serialize
from map.forms import *
from inmobiliaria.models import Lugar,provinceChoice,ubicationChoice
from map.is_in_polygon import inpolygon

# Create your views here.
def index(request):
    
    db_maps=Map('./db.mbtiles')
    a= db_maps.get_Image(2,1,1)    
    Places_alq= FindPlaces_alquiler()
    Places_vent= FindPlaces_venta()
    Places_generic= GenericSearch()
    return render(request,'mapa/index_client.html',{'form0':Places_alq,'form1':Places_vent,'form2':Places_generic})

def index2(request,zoom,col,row):
    db_maps=Map('./db.mbtiles')
    a= db_maps.get_Image(int(zoom),int(col),int(row))    
    return HttpResponse(a,content_type='image/x-png')

def markers(request):
    
    remove=request.GET.get('remove','')
    lat1=request.GET.get('lat','')
    lng1=request.GET.get('lng','')
    namea=request.GET.get('name','sin nombre')
    typee=request.GET.get('type','')
    icon=request.GET.get('icon','')
    id=request.GET.get('id','')
    
    if remove:
        q=marker.objects.get(lat=lat1,lng=lng1)
        q.delete()
    elif id:  #si pasa el id del marcador es para actualizar su posición
        q= marker.objects.get(id=id)
        q.lat=lat1
        q.lng=lng1
        q.save()
    else:            
        q=marker(name=namea, icon=icon,lat=lat1,lng=lng1,place=c[0])
        q.save()
    
    return HttpResponse()


def spacial_selec(request):
    
    alquiler=request.GET.get('alq','')#
    alquilerXcuarto=request.GET.get('alqXcuart','')
    min_alq=request.GET.get('min_alq','100')#
    max_alq=request.GET.get('max_alq','1000000')#
    vent=request.GET.get('vent','')#
    subastable=request.GET.get('subs','')
    min_vent=request.GET.get('min_vent','100000')#
    max_vent=request.GET.get('max_vent','10000000000')#
    prov=request.GET.get('prov','')
    poly=request.GET.get('poly','')
    
    #consulta de las casas para alquilar
    
    result=Lugar.objects.filter(
                                precio_de_alquiler__gte=min_alq,
                                precio_de_alquiler__lte=max_alq
                                ).filter(
                                precio_de_venta__gte=min_vent,
                                precio_de_venta__lte=max_vent
                                ).filter(
                                subastable=subastable
                                )
    if prov!='A':
        result=result.filter(provincia=prov)

    if alquiler=='True' and vent=='False':
        result=result.filter(
            venta_o_renta='Renta linear'
        )
    elif alquiler=='False' and vent=='True':
        result=result.filter(
            venta_o_renta='Venta'
        )#falta la otra renta

    if poly=='True':
        result2=set()
        points= parse(request.GET.get('latlengs',''))
        for item in points:
           result2= result2.union(polygon_search(item,result))
        json =serialize('json',result2,fields=['id','descripcion','foto1','precio_de_venta','precio_de_alquiler','venta_o_renta','nombre','lat','lng'])
    else:
        json =serialize('json',result,fields=['id','descripcion','foto1','precio_de_venta','precio_de_alquiler','venta_o_renta','nombre','lat','lng'])
        

       
    return HttpResponse(json,content_type='application/json')

def parse(points):
    points=points.split('|')
    sets_of_points=[]
    for item in points:
        a=item.split('_')
        a.pop()
        sets_of_points+=[a]

    # print(sets_of_points)
    sets_of_points.pop()
    return sets_of_points

#este metodo no es una vista, lo q le paso request para obtener los parametros que me hacen falta
def polygon_search(points,selected_house):
    # latlengs=request.GET.get('latlengs','')

    # latlengs = latlengs.split('_')
    # latlengs.pop()

    
    minLat=24
    maxLat=20
    minLng=-75
    maxLng=-90
    for i in range(len(points)):
        item = points[i].split(',')
        points[i]=[float(item[0]),float(item[1])]
        
        if points[i][0]<minLat:
            minLat=points[i][0]
        elif points[i][0]>maxLat:
            maxLat=points[i][0]        
        if points[i][1]<minLng:
            minLng=points[i][1]
        elif points[i][1]>maxLng:
            maxLng=points[i][1]
    # points es la lista de los puntos del poligono

    # selected_house= selected_house.filter(lat__gt=minLat).filter(lat__lt=maxLat).filter(lng__lt=maxLng).filter(lng__gt=minLng)#(lat__lt=minLat,,lat__gt=maxLat,lng__lt=maxLng,lng__gt=minLng)
    result=[]

    ##AQUI PONER EL ALGORITMO BUENO
    points.append(points[0])
    for i in selected_house:
        if inpolygon(float(i.lat),float(i.lng),points):
            result.append(i)
    
    return result

#hacer los filtros para mandar las casas 
def json_view(request):    
    casas=Lugar.objects.all()
    json =serialize('json',casas,fields=['id','descripcion','foto1','precio_de_venta','precio_de_alquiler','venta_o_renta','nombre','lat','lng'])
       
   
    return HttpResponse(json,content_type='application/json')

def json_view_id(request,id):    
    print("--------------------------------------------------------------")
    casas=Lugar.objects.filter(id = id)
    json =serialize('json',casas,fields=['id','descripcion','foto1','precio_de_venta','precio_de_alquiler','venta_o_renta','nombre','lat','lng'])
    print(casas)
    return HttpResponse(json,content_type='application/json')