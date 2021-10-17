var map = L.map('mapid').setView([23.10089, -82.33297], 12);
//https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png
var trib = L.tileLayer('/map/{id}/{z}/{x}/{y}.png', {
    // var trib = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 18,
    minZoom: 8,
    attribution: 'Keep Calm',
    id: 'test',
    reuseTiles: true,
}).addTo(map);





$(".event_search").change(clk_poly);

function add() {
    var val = window.location.pathname.split('/');
    if (val[1] == "pubs") {
        addMarker(val[3]);
    } else if (val[1] == "recorrido") {

        $.getJSON("/recorridojson/" + val[2], print_recorrido);

    } else {

        addMarkers();
    }

}

function print_recorrido(data) {
    var points = [];
    for (var i = 0; i < data.length; i++) {

        points.push(L.latLng([data[i].fields['lat'], data[i].fields['lng']]));
    }
    L.Routing.control({
        waypoints: points,
        routeWhileDragging: true
    }).addTo(map);
}

$(document).ready(add());

/*Marca de Agua*/

L.Control.Watermark = L.Control.extend({
    onAdd: function(map) {
        var img = L.DomUtil.create('img');

        img.src = '/static/mapa/assets/leaflet/images/logo.png';
        img.style.width = '100px';
        img.style.opacity = '0.65';
        // img.style.background = 'gray';

        return img;
    },

    onRemove: function(map) {
        // Nothing to do here
    }
});

L.control.watermark = function(opts) {
    return new L.Control.Watermark(opts);
}

L.control.watermark({ position: 'bottomleft' }).addTo(map);
/**/

function addMarkers() {

    $.getJSON("/map/json", add_MarkerJson);

}

function addMarker(id) {

    $.getJSON("/map/mijson/" + id, add_one_MarkerJson);

}

var markers;

function filter_House(data) {
    try {
        markers.remove();
    } catch (error) {

    }
    markers = new L.MarkerClusterGroup();
    var markersList = [];

    for (var i = 0; i < data.length; i++) {
        //crear un icono un una clase css
        var myIcon = L.divIcon({
            className: 'glyphicon glyphicon-home size20',
        });

        var mar = L.marker([data[i].fields['lat'], data[i].fields['lng']], {
            icon: myIcon,
            fillColor: 'red',
            fillOpacity: 0.5,
            riseOnHover: true,
            alt: data[i].pk,

        });

        //RECORDAR PONER EL LINK A LA CASA CON TODA SU INFORMACION
        mar.bindPopup("<a href='/'><img src='/media/" + data[i].fields['foto1'] + "' heigth=400px width=300px></a><br>" + data[i].fields['descripcion']);

        markersList.push(mar);
        markers.addLayer(mar);

    }

    map.addLayer(markers);

}

function add_one_MarkerJson(data) {
    markers = new L.MarkerClusterGroup();
    var markersList = [];

    for (var i = 0; i < data.length; i++) {
        //crear un icono un una clase css

        if (data[i].fields['venta_o_renta'] == 'Venta') {

            var myIcon = L.divIcon({
                className: 'glyphicon glyphicon-home size20',
            });
        } else {
            var myIcon = L.divIcon({
                className: 'glyphicon glyphicon-heart size20',
            });
        }

        var mar = L.marker([data[i].fields['lat'], data[i].fields['lng']], {
            icon: myIcon,
            fillColor: 'red',
            fillOpacity: 0.5,
            //lo puedes mover de lugar
            //draggable: true,
            //titulo cuando se pone el mouse arriba
            title: data[i]["fields"].name,
            //se pinta por encima de los otros marcadores
            riseOnHover: true,
            alt: data[i].pk,

        });

        // map = L.map('mapid').setView([data[i].fields['lat'], data[i].fields['lng']], 12);

        //https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png
        // trib = L.tileLayer('/map/{id}/{z}/{x}/{y}.png', {
        //     maxZoom: 18,
        //     minZoom: 8,
        //     attribution: 'Keep Calm',
        //     id: 'test',
        //     reuseTiles: true,
        // }).addTo(map);

        markersList.push(mar);
        markers.addLayer(mar);

    }

    map.addLayer(markers);

}

function add_MarkerJson(data) {

    markers = new L.MarkerClusterGroup();
    var markersList = [];

    for (var i = 0; i < data.length; i++) {
        //crear un icono un una clase css

        var content = "<h4>" + data[i].fields['nombre'] + "</4><a href='/pubs/places/" + data[i].pk + "'><img src='/media/" + data[i].fields['foto1'] + "' heigth=400px width=300px></a><br>" + data[i].fields['descripcion'] + "</p><p><b>Precio:</b>";
        if (data[i].fields['venta_o_renta'] == 'Venta') {

            var myIcon = L.divIcon({
                className: 'glyphicon glyphicon-home size20',
            });
            content += data[i].fields['precio_de_venta'] + "</p>";
        } else {
            var myIcon = L.divIcon({
                className: 'glyphicon glyphicon-heart size20',
            });
            content += data[i].fields['precio_de_alquiler'] + "</p>";
        }

        var mar = L.marker([data[i].fields['lat'], data[i].fields['lng']], {
            icon: myIcon,
            fillColor: 'red',
            fillOpacity: 0.5,
            //lo puedes mover de lugar
            //draggable: true,
            //titulo cuando se pone el mouse arriba
            title: data[i]["fields"].name,
            //se pinta por encima de los otros marcadores
            riseOnHover: true,
            alt: data[i].pk,

        });
        mar.bindPopup(content);
        markersList.push(mar);
        markers.addLayer(mar);

    }

    map.addLayer(markers);


}


var pol_points = [
    []
];
var index_poly = 0;
var open_poly = false;
var polygon = [L.polygon([
    [0, 0]
], { color: 'blue' }).addTo(map)];
var clean = false;
var count = 0;
var layerPolig = L.layerGroup();

var mar = '';

function onMapClick(e) {

    if (window.location.pathname != '/map/' && window.location.pathname.split("/")[1] != 'recorrido') {

        var myIcon = L.divIcon({
            className: 'glyphicon glyphicon-home size20',
        });

        if (mar != '') {
            mar.remove();
        }

        mar = L.marker([e.latlng.lat, e.latlng.lng], {
            icon: myIcon,
            fillColor: 'red',
            fillOpacity: 0.5
        });

        mar.addTo(map)
        $('#id_lat')[0].value = e.latlng.lat;
        $('#id_lng')[0].value = e.latlng.lng;

    } else {
        var poligono = $("#id_buscar_Area")[0].checked;
        if (poligono) {

            if (clean) {
                if (count == 1) {
                    layerPolig.remove()
                    layerPolig = L.layerGroup();
                    clean = false;
                    count = 0;
                    pol_points = [
                        []
                    ];
                } else {

                    count++;
                }
            }

            open_poly = true;

            pol_points[index_poly].push(e.latlng);
            polygon[index_poly] = L.polyline(pol_points[index_poly], {
                color: 'silver',
                smoothFactor: 2.0,
                weight: 8

            });

            // var circle = L.circle(e.latlng, 200, {
            //     color: 'white',
            //     fillColor: 'silver',
            //     fillOpacity: 0.5
            // });

            layerPolig.addLayer(polygon[index_poly]);

            layerPolig.addTo(map);


        } else {
            layerPolig.remove()
            layerPolig = L.layerGroup();
            clean = false;
            count = 0;
            pol_points = [
                []
            ];
        }
    }



}

function Close_Polygon() {

    var poligono = $("#id_buscar_Area")[0].checked;
    if (poligono) {

        pol_points[index_poly].push(pol_points[index_poly][0]);
        polygon[index_poly] = L.polyline(pol_points[index_poly], {
            color: 'silver',
            smoothFactor: 2.0,
            weight: 15

        });

        // var circle = L.circle(e.latlng, 200, {
        //     color: 'white',
        //     fillColor: 'silver',
        //     fillOpacity: 0.5
        // });

        layerPolig.addLayer(polygon[index_poly]);
        // layerPolig.addLayer(circle);

        layerPolig.addTo(map);

        open_poly = false;

        clk_poly();

    }


}

function Add_Polygon() {

    if (open_poly) {
        Close_Polygon()
    }
    pol_points.push([]);
    index_poly++;

}

function onMapMove(e) {

    $("#xxx").text(e.latlng);

}

function clk(e) {
    var rad4 = document.getElementById("r4");
    if (rad4.checked) {
        this.remove();
    }
}

function clk_poly() {

    var element = "";
    // clean = true;
    for (var j = 0; j < polygon.length; j++) {
        for (var i = 0; i < polygon[j]._latlngs.length; i++) {
            element += polygon[j]._latlngs[i].lat + ",";
            element += polygon[j]._latlngs[i].lng + "_";
        }
        element += "|"

    }
    map.removeLayer(markers);
    $.getJSON("spacselect", {
        latlengs: element,
        alq: $("#id_renta_linear")[0].checked ? "True" : "False",
        alqXcuart: $("#id_renta_de_cuartos")[0].checked ? "True" : "False",
        min_alq: $("#id_min_precioAlquiler")[0].value,
        max_alq: $("#id_max_precioAlquiler")[0].value,
        vent: $("#id_venta")[0].checked ? "True" : "False",
        subs: $("#id_subastable")[0].checked ? "True" : "False",
        min_vent: $("#id_min_precioVenta")[0].value,
        max_vent: $("#id_max_precioVenta")[0].value,
        prov: $("#id_provincia")[0].value,
        poly: $("#id_buscar_Area")[0].checked ? "True" : "False",
    }, add_MarkerJson);
    // $.get("spacselect", { latlengs: element },add_MarkerJson);

}

map.on('click', onMapClick);
map.on('mousemove', onMapMove);


$("#a").click(function() {
    $("#form_map").slideToggle("slow");
});
