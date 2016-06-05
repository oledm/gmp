(function() {
    'use strict';

    angular
        .module('app.dashboard')
        .controller('DashboardController', DashboardController);

    function DashboardController(History) {
        'ngInject';

        var vm = this;

        vm.list = [];

        History.list()
            .then(data => vm.list = data);
    }
})();
