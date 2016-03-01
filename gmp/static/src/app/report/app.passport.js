(function() {
    'use strict';

    angular
        .module('app.passport')
        .controller('PassportController', PassportController);

    PassportController.$inject = ['UserData'];
    function PassportController(UserData) {
        var vm = this,
            ranks = [
                'руководитель бригады',
                'зам. руководителя бригады',
                'член бригады'
            ];

        vm.addEmployee = addEmployee;
        vm.allEmployees = [];
        vm.ranks = ranks;
        vm.team = [{'name': '', 'required': 'required'}];

        activate();

        //////////////////////////

        function activate() {
            getEmployees();
        }

        function addEmployee() {
//            console.log('team: ' + JSON.stringify(vm.team));
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
