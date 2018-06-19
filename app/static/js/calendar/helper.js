angular
  .module('mwl.calendar.docs')
  .factory('alert', function($uibModal) {

    function show(action, event) {
      return $uibModal.open({
        template: `
        <div class="modal-header">
          <h3 class="modal-title">Event action occurred!</h3>
        </div>
        <div class="modal-body">
          <p>Action:
            <pre>{{ vm.action }}</pre>
          </p>
          <p>Event:
            <pre>{{ vm.event | json }}</pre>
          </p>
        </div>
        <div class="modal-footer">
          <button class="btn btn-primary" ng-click="$close()">OK</button>
        </div>
        `,
        controller: function() {
          var vm = this;
          vm.action = action;
          vm.event = event;
        },
        controllerAs: 'vm'
      });
    }

    return {
      show: show
    };

  });
