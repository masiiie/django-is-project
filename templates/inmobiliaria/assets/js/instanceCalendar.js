var todayDate = moment().startOf('day');
var YM = todayDate.format('YYYY-MM');
var YESTERDAY = todayDate.clone().subtract(1, 'day').format('YYYY-MM-DD');
var TODAY = todayDate.format('YYYY-MM-DD');
var TOMORROW = todayDate.clone().add(1, 'day').format('YYYY-MM-DD');
var FIRST_DAY = new Date(Number(TODAY.split('-')[0]),Number(TODAY.split('-')[1]-1),1).toISOString().split('T')[0]
var LAST_DAY = new Date(Number(TODAY.split('-')[0]),Number(TODAY.split('-')[1]-1),[0,31, (!(Number(TODAY.split('-')[0])&3||Number(TODAY.split('-')[0])&15&&!(Number(TODAY.split('-')[0])%25)) ? 29 : 28), 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][Number(TODAY.split('-')[1])]).toISOString().split('T')[0]

var a = window.location.toString().split("/");
  $.get("/dateintersection/"+FIRST_DAY+'/'+LAST_DAY+'/'+a[a.length - 1], function (data, status) {
    $('#calendar').fullCalendar({
      selectable: true,
      header: {
        left: 'prev,next today',
        center: 'title',
        right: 'month,agendaWeek,agendaDay'
      },
      events: data,
      dayClick: function (date) {
        alert('clicked ' + date.format());
      },
      select: function (startDate, endDate) {
        var a = window.location.toString().split("/");
        $.get("/dateintersection/" + startDate.format() + "/" + endDate.format() + "/" + a[a.length - 1], function (data) {
          $('#calendar').hide();
          $('#calendar2').fullCalendar({
  
            defaultView: 'month',
            header: {
              left: 'prev,next today',
              center: 'title',
              right: 'month,agendaWeek,agendaDay'
            },
            //editable: true,
            eventLimit: true, // allow "more" link when too many events
            navLinks: true,
            events: data,
  
          });
  
        });
        //alert('selected ' + startDate.format() + ' to ' + endDate.format());
      }
    });
  });

  /* Calendario de seleccion */
  

