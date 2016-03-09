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
            engine = {
                all: [],
                selected: {
                    'type': '',
                    'serial_number': 0
                },
                sortOrder: 'name'
            };

        vm.addEmployee = addEmployee;
        vm.allEmployees = [];
        vm.createPassport = createPassport;
        vm.engine = engine;
        vm.investigationDate = undefined;
        vm.lpus = {};
        vm.measurers = measurers;
        vm.ranks = ranks;
        vm.report = {
            team: [{'name': '', 'required': 'required'}],
            measurers: measurers.selected
        };
        

        activate();

        //////////////////////////

        function activate() {
//            createPassport();
            getEmployees();
            getEngines();
            getLPUs();
        }

        function addEmployee() {
//            console.log('team: ' + JSON.stringify(vm.team));
            vm.report.team.push({
                'name': ''
            });
        }
        function createPassport() {
            delete vm.report.team[0].required;
            vm.report.investigationDate = vm.investigationDate.toLocaleString();
            Passport.createPassport(vm.report);
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
                    vm.engine.all = data;
                });
        }

        function getLPUs() {
            Passport.getLPUs()
                .then(function(data) {
                    vm.lpus = data;
                });
        }

    }
})();
