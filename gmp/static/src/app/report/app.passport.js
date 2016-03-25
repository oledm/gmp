(function() {
    'use strict';

    angular
        .module('app.passport')
        .controller('PassportController', PassportController);

    PassportController.$inject = ['$scope', 'UserData', 'Department', 'Engine', 'Passport', 'Upload'];
    function PassportController($scope, UserData, Department, Engine, Passport, Upload) {

        $scope.upload = upload;


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
        vm.enterValue = enterValue;
        vm.setSelected = setSelected;
        vm.workBegin = undefined;
        vm.workEnd = undefined;
        vm.investigationDate = undefined;
        vm.lpus = {};
        vm.orgs = {};
        vm.tclasses = {all: [], selected: ''};
        vm.getLPUs = getLPUs;
        vm.measurers = measurers;
        vm.ranks = ranks;
        vm.report = {
            team: [{'name': '', 'required': true}],
            measurers: measurers.selected,
            docs: docs,
            files: {},
            therm: {},
            vibro: {},
            resistance: {}
        };

        activate();

        //////////////////////////

        function upload(element) {
            var fieldname = element.name;
            angular.forEach(element.files, function(file) {
                Upload.upload({
                    url: '/api/upload/',
                    data: {fileupload: file}
                }).
                then(function(response) {
                    vm.report.files[fieldname] = response.data.id;
                }, function(response) {
                    console.log('Error status: ' + response.status);
                });
            });
        }

        function activate() {
            getEmployees();
            getEngines();
            getOrgs();
            getTClasses();
        }

        function addEmployee() {
            vm.report.team.push({
                'name': '', 'required': false
            });
            console.dir('team: ' + JSON.stringify(vm.report.team));
        }
        function createPassport() {
            console.log('investigationDate ' + vm.investigationDate.toLocaleString());
            console.log('begin ' + vm.workBegin.toLocaleString());
            console.log('end ' + vm.workEnd.toLocaleString());
//            return;
//            delete vm.report.team[0].required;
//            vm.report.therm.tclass = vm.tclasses.all.filter(function(el) {
//                return el.name === vm.tclasses.selected;
//            })[0].id;
//            console.dir('selected class: ' + JSON.stringify(vm.report.therm));
//            vm.report.investigationDate = vm.investigationDate.toLocaleString();
//            vm.report.engine.new_date = vm.report.engine.new_date.toLocaleString();
//            vm.report.workBegin = vm.workBegin.toLocaleString();
//            vm.report.workEnd = vm.workEnd.toLocaleString();
//
//            Passport.createPassport(vm.report);
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

        function getTClasses() {
            Passport.getTClasses()
                .then(function(data) {
                    vm.tclasses.all = data;
                });
        }

        function enterValue(event, param, prop) {
            event.stopPropagation();

            var promise = $mdEditDialog.small({
                modelValue: param[prop],
                placeholder: 'Введите значение',
                save: function (input) {
                param[prop] = input.$modelValue;
            },
            targetEvent: event,
            validators: {
                'md-maxlength': 30,
                'ng-pattern': '/^[0-9.,]*$/'
            },
            messages: {
                'md-maxlength': 'Слишком большое значение',
                'required': 'Обязательное значение'
            }
            });

            promise.then(function (ctrl) {
                var input = ctrl.getInput();

                input.$viewChangeListeners.push(function () {
                input.$setValidity('test', input.$modelValue !== 'test');
                });
            });
        }

        function setSelected(selected, item) {
            var id = item.id,
                index = selected.indexOf(id);
            if (index !== -1) {
                selected.splice(index, 1);
                item['selected'] = false;
            } else {
                item['selected'] = true;
                selected.push(id);
            }
            console.log('Выбраны приборы с id ' + JSON.stringify(selected));
        }
    }
})();
