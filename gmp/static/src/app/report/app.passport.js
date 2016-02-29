(function() {
    'use strict';

    angular
        .module('app.passport')
        .controller('PassportController', PassportController);

    PassportController.$inject = ['UserData'];
    function PassportController(UserData) {
        var vm = this;

        vm.addEmployee = addEmployee;
        vm.allEmployees = [];
        vm.team = [{'name': ''}];

        activate();

        //////////////////////////

        function activate() {
            getEmployees();
        }

        function addEmployee() {
            vm.team.push({
                'name': ''
            });
        }

        function getEmployees() {
            UserData.getAllUsers()
                .then(function(data) {
                    vm.allEmployees = data;
                });
        }
    }
})();
