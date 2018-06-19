angular.module('mwl.calendar.docs', ['mwl.calendar', 'ngAnimate', 'ui.bootstrap', 'colorpicker.module']);
var data;
var abc = 'abcde';

angular
  .module('mwl.calendar.docs') //you will need to declare your module with the dependencies ['mwl.calendar', 'ui.bootstrap', 'ngAnimate']
  .controller('KitchenSinkCtrl', function(moment, alert, calendarConfig,$timeout) {

    // 發送 Ajax 查詢請求並處理
  var request = new XMLHttpRequest();
  request.open("GET", "api/events");
  request.send();

  request.onreadystatechange = function() {
      // 伺服器請求完成
      if (request.readyState === 4) {
          // 伺服器回應成功
          if (request.status === 200) {
              var type = request.getResponseHeader("Content-Type");   // 取得回應類型

              // 判斷回應類型，這裡使用 JSON
              if (type.indexOf("application/json") === 0) {               
                  data = JSON.parse(request.responseText);
                  console.log(data);
              }
          } else {
              alert("發生錯誤: " + request.status);
          }
      }
    }

    var vm = this;   
    var notpush = true;
    //These variables MUST be set as a minimum for the calendar to work
    vm.calendarView = 'month';
    vm.title = moment(vm.viewDate).format('YYYY');
    console.log(vm.title);
    vm.viewDate = new Date();
      vm.events = [];

    vm.cellIsOpen = true;

    vm.GetGoogleData = function(){
      gapi.client.calendar.events.list({
        'calendarId': 'primary',
        'timeMin': (new Date()).toISOString(),
        'showDeleted': false,
        'singleEvents': true,
        'maxResults': 150,
        'orderBy': 'startTime'
      }).then(function(response) {
        var events = response.result.items;

        //the json that you want kc <3
        var jsons = {"data":[]}                           
        if (events.length > 0) {
          for (i = 0; i < events.length; i++) {
            var event = events[i];
            // start time
            var when_start = event.start.dateTime;
            if (!when_start) {
              when_start = event.start.date+'T00:00:00+08:00';
            }
            // end time
            var when_end = event.end.dateTime;
            if (!when_end) {
              when_end = event.end.date+'T00:00:00+08:00';
            }
            // jsons["data"].push({"title":event.summary,
            // "starttime":when_start,
            // "endtime":when_end})
            new_data = {
              title: event.summary,
              startsAt: moment(when_start).toDate(),
              endsAt: moment(when_end).toDate(),
              color: calendarConfig.colorTypes.important,
              draggable: true,
              resizable: true
            };
            console.log(new_data);
            new_post_data = 
              '&title='+ event.summary +
              '&starttime=' + moment(when_start).utc().format('YYYY-MM-DD HH:mm') +
              '&endtime=' + moment(when_end).utc().format('YYYY-MM-DD HH:mm') +
              '&p_color=' + new_data.color.primary +
              '&s_color=' + new_data.color.secondary +
              '&comment=' + '';
            vm.events.push(new_data);
            var request = new XMLHttpRequest();
            request.open('POST', 'api/add_event');
            request.setRequestHeader("Content-Type", 'application/x-www-form-urlencoded');
            request.send(new_post_data);
          }
        }
      });
    }

    vm.addEvent = function(csrf_token) {
      new_data = {
        title: 'New event',
        startsAt: moment().startOf('day').toDate(),
        endsAt: moment().endOf('day').toDate(),
        color: calendarConfig.colorTypes.important,
        draggable: true,
        resizable: true
      };
      new_post_data = 
        'csrfmiddlewaretoken='+ csrf_token +
        '&title='+ 'New event' +
        '&starttime=' + moment().startOf('day').utc().format('YYYY-MM-DD HH:mm') +
        '&endtime=' + moment().endOf('day').utc().format('YYYY-MM-DD HH:mm') +
        '&p_color=' + new_data.color.primary +
        '&s_color=' + new_data.color.secondary +
        '&comment=' + '';
      vm.events.push(new_data);
      var request = new XMLHttpRequest();
      request.open('POST', 'api/add_event');
      request.setRequestHeader("Content-Type", 'application/x-www-form-urlencoded');
      request.send(new_post_data);
    };
    
    vm.eventClicked = function(event) {
      console.log('Clicked')
      alert.show('Clicked', event);
    };

    vm.eventEdited = function(event) {
      console.log('Edited');
      alert.show('Edited', event);
    };

    vm.eventDeleted = function(event) {
      alert.show('Deleted', event);
    };

    vm.eventTimesChanged = function(event) {
      console.log(vm.events);
      alert.show('Dropped or resized', event);
    };

    vm.modifyCell = function(calendarCell){
      if(notpush){
          if(data){
            for (i in data.data){
              vm.events.push({
                event_id : data.data[i].event_id,
                title: data.data[i].title,
                startsAt: new Date(moment.unix(data.data[i].starttime)),
                endsAt: new Date(moment.unix(data.data[i].endtime)),
                color: {
                  primary: data.data[i].p_color,
                  secondary: data.data[i].s_color
                },
                draggable: false,
                resizable: false
              });
              notpush = false;
              // console.log(data);
              // console.log(vm.events)
              }
          }
        }
      }

    vm.eventTimesChanged = function(calendarEvent){
      console.log(calendarEvent);
    }

    vm.toggle = function($event, field, event) {
      $event.preventDefault();
      $event.stopPropagation();
      event[field] = !event[field];
    };

    vm.timespanClicked = function(date, cell) {
      if (vm.calendarView === 'month') {
        if ((vm.cellIsOpen && moment(date).startOf('day').isSame(moment(vm.viewDate).startOf('day'))) || cell.events.length === 0 || !cell.inMonth) {
          vm.cellIsOpen = false;
        } else {
          vm.cellIsOpen = true;
          vm.viewDate = date;
        }
      } else if (vm.calendarView === 'year') {
        if ((vm.cellIsOpen && moment(date).startOf('month').isSame(moment(vm.viewDate).startOf('month'))) || cell.events.length === 0) {
          vm.cellIsOpen = false;
        } else {
          vm.cellIsOpen = true;
          vm.viewDate = date;
        }
      }

    };  
    vm.delete_data = function(event){
      console.log(event.event_id);
      const del_link = "api/del_event/" + event.event_id;
      console.log(del_link);
      var request = new XMLHttpRequest();
      request.open("GET", del_link);
      request.send();
    }
    vm.save_data = function(event,csrf_token){
      console.log(event.color);
      post_data = 
        'csrfmiddlewaretoken='+ csrf_token +
        '&event_id=' + event.event_id +
        '&title='+ event.title +
        '&starttime=' + moment(event.startsAt).utc().format('YYYY-MM-DD HH:mm') +
        '&endtime=' + moment(event.endsAt).utc().format('YYYY-MM-DD HH:mm') +
        '&p_color=' + event.color.primary +
        '&s_color=' + event.color.secondary +
        '&comment=' + '';
      var request = new XMLHttpRequest();
      request.open('POST', 'api/update_event');
      request.setRequestHeader("Content-Type", 'application/x-www-form-urlencoded');
      request.send(post_data);
      console.log(request);
    }
    var auto = $timeout(function() {
      vm.modifyCell();
    },1000);
  })
  .config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[{');
    $interpolateProvider.endSymbol('}]}');
  });