(function() {
    'use strict';

    angular
        .module('app.passport')
        .controller('PassportController', PassportController);

    PassportController.$inject = ['UserData', 'Department', 'Engine', 'Passport'];
    function PassportController(UserData, Department, Engine, Passport) {
        var vm = this,
            docs = [
                {name: 'Журнал ремонта электродвигателя', value: true},
                {name: 'Журнал эксплуатации электродвигателя', value: true},
                {name: 'Инструкция по эксплуатации завода-изготовителя', value: true},
                {name: 'Протоколы штатных измерений и испытаний', value: true},
                {name: 'Паспорт завода-изготовителя на взрывозащищенный электродвигатель', value: true},
                {name: 'Схема электроснабжения электродвигателя', value: true}
            ],
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
        vm.workBegin = undefined;
        vm.workEnd = undefined;
        vm.investigationDate = undefined;
        vm.lpus = {};
        vm.orgs = {};
        vm.getLPUs = getLPUs;
        vm.measurers = measurers;
        vm.ranks = ranks;
        vm.report = {
            team: [{'name': '', 'required': 'required'}],
            measurers: measurers.selected,
            docs: docs
        };

        activate();

        //////////////////////////

        function activate() {
            getEmployees();
            getEngines();
            getOrgs();
        }

        function addEmployee() {
            vm.report.team.push({
                'name': ''
            });
        }
        function createPassport() {
            delete vm.report.team[0].required;
            vm.report.investigationDate = vm.investigationDate.toLocaleString();
            vm.report.workBegin = vm.workBegin.toLocaleString();
            vm.report.workEnd = vm.workEnd.toLocaleString();
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

        function getOrgs() {
            Passport.getOrgs()
                .then(function(data) {
                    vm.orgs = data;
                });
        }

        function getLPUs(orgName) {
            var organ = vm.orgs.filter(function(el) {
                return el.name === orgName;
            });

            Passport.getLPUs(organ[0].id)
                .then(function(data) {
                    vm.lpus = data;
                });
        }
    }
})();
