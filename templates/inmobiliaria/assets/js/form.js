temp = 0;
function onFormMapClick(e) {
    if (temp!= 0) temp.remove();
    /*punto*/
    var icono = "glyphicon glyphicon-home size20";
    var icon_coust = L.divIcon({
        className: icono,
    });

    temp = L.marker(e.latlng, {
        icon: icon_coust,
        fillColor: '#f03',
        fillOpacity: 0.5,
        //lo puedes mover de lugar
        draggable: true,
        //titulo cuando se pone el mouse arriba
        title: "Marcador con titulo",
        //se pinta por encima de los otros marcadores
        riseOnHover: true,
    })
    temp.addTo(map);//.bindPopup(x.value).on('click', clk);
    document.getElementById('x_input').value = e.latlng.lat
    document.getElementById('y_input').value = e.latlng.lng

    // $.get("markers", { lat: e.latlng.lat, lng: e.latlng.lng, name: x.value, type: "Alquiler", icon: icono });


}
map.on('click', onFormMapClick);
