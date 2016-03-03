(function() {
    'use strict';

    angular
        .module('app.passport')
        .controller('PassportController', PassportController);

    PassportController.$inject = ['UserData', 'Department', 'Engine', 'Passport'];
    function PassportController(UserData, Department, Engine, Passport) {
        var vm = this,
            ranks = [
                'руководитель бригады',
                'зам. руководителя бригады',
                'член бригады'
            ],
            measurers = {
                all: Department.measurers(),
                selected: [],
                sortOrder: 'name'
            },
            engines = {
                all: [],
                selected: '',
                sortOrder: 'name'
            };

        vm.addEmployee = addEmployee;
        vm.allEmployees = [];
//        vm.createPassport = createPassport;
        vm.measurers = measurers;
        vm.engines = engines;
        vm.ranks = ranks;
        vm.team = [{'name': '', 'required': 'required'}];

        activate();

        //////////////////////////

        function activate() {
            createPassport();
            getEmployees();
            getEngines();
        }

        function addEmployee() {
//            console.log('team: ' + JSON.stringify(vm.team));
            vm.team.push({
                'name': ''
            });
        }
        function createPassport() {
            return Passport.createPassport().
                then(function(response) {
                    return response;
                });
        }

        function getEmployees() {
            UserData.getAllUsers()
                .then(function(data) {
                    vm.allEmployees = data;
                });
        }

        function getEngines() {
            Engine.getAllEngines()
                .then(function(data) {
                    vm.engines.all = data;
                });
        }
    }
})();
