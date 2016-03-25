(function() {
    'use strict';

    angular.module('app.datepicker')
        .controller('DatepickerController', DatepickerController);

    DatepickerController.$inject = ['uibDatepickerPopupConfig'];

    function DatepickerController(uibDatepickerPopupConfig) {
        var vm = this;

        uibDatepickerPopupConfig.closeText = 'Закрыть';
        uibDatepickerPopupConfig.currentText = 'Сегодня';
        uibDatepickerPopupConfig.clearText = 'Очистить';


        vm.dateOptions = {
          formatYear: 'yy',
          startingDay: 1,
        };

        vm.open = function() {
          vm.popup.opened = true;
        };

        vm.setDate = function(year, month, day) {
          vm.dt = new Date(year, month, day);
        };

        vm.formats = ['dd-MMMM-yyyy', 'yyyy/MM/dd', 'dd.MM.yyyy', 'shortDate'];
        vm.format = vm.formats[0];
        vm.altInputFormats = ['M!/d!/yyyy'];

        vm.popup = {
          opened: false
        };

        var tomorrow = new Date();
        tomorrow.setDate(tomorrow.getDate() + 1);
        var afterTomorrow = new Date();
        afterTomorrow.setDate(tomorrow.getDate() + 1);
        vm.events = [
          {
            date: tomorrow,
            status: 'full'
          },
          {
            date: afterTomorrow,
            status: 'partially'
          }
        ];

        function getDayClass(data) {
          var date = data.date,
            mode = data.mode;
          if (mode === 'day') {
            var dayToCheck = new Date(date).setHours(0,0,0,0);

            for (var i = 0; i < vm.events.length; i++) {
              var currentDay = new Date(vm.events[i].date).setHours(0,0,0,0);

              if (dayToCheck === currentDay) {
                return vm.events[i].status;
              }
            }
          }

          return '';
        }
    }

})();
