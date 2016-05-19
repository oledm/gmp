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
        uibDatepickerPopupConfig.type = 'month';

        vm.dateOptions = {
            startingDay: 1
        };

        vm.yearOptions = {
            datepickerMode: 'year',
            maxMode: 'year',
            minMode: 'year',
            formatYear: 'yyyy'
        };

        vm.open = function() {
          vm.popup.opened = true;
        };

        vm.popup = {
          opened: false
        };
    }
})();
