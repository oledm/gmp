(function() {
    'use strict';

    angular
        .module('app.passport')
        .controller('PassportController', PassportController);

    PassportController.$inject = ['$scope', '$state', 'UserData', 'Department', 'Engine', 'Passport', 'Upload'];
    function PassportController($scope, $state, UserData, Department, Engine, Passport, Upload) {

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

        vm.pages = [
            'team.tpl.html',
            'measurers.tpl.html',
            'lpu.tpl.html',
            'dates.tpl.html',
            'engines.tpl.html',
            'values.tpl.html',
            'docs.tpl.html',
            'photos.tpl.html',
            'therm.tpl.html',
            'vibro.tpl.html',
            'resistance.tpl.html',
            'signers.tpl.html'
        ];

        if ($state.is('passport')) {
            vm.reportType = 'паспорта двигателя';
            vm.buttonText = 'паспорт';
        } else if ($state.is('report')) {
            vm.reportType = 'экспертного заключения';
            vm.buttonText = 'заключение';
        }


        vm.addEmployee = addEmployee;
        vm.allEmployees = [];
        vm.createPassport = createPassport;
        vm.engine = engine;
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
//            console.dir('team: ' + JSON.stringify(vm.report.team));
        }
        function createPassport() {

//            console.log('docs ' + JSON.stringify(vm.report.docs));
//            console.log('investigationDate ' + vm.investigationDate.toLocaleString());
//            console.log('begin ' + vm.workBegin);
//            console.log('end ' + vm.workEnd.toLocaleString());
//            Passport.createPassport(vm.workBegin);
//            return;
            delete vm.report.team[0].required;
            console.dir('vm.tclasses.all: ' + JSON.stringify(vm.tclasses.all));
            vm.report.therm.tclass = vm.tclasses.all.filter(function(el) {
                return el.name === vm.tclasses.selected;
            })[0].id;
            console.dir('selected class: ' + JSON.stringify(vm.report.therm));

//            var datefilter = $filter('date'),
//                dateFormat = 'dd.MM.yyyy';
//            vm.report.investigationDate = datefilter(vm.investigationDate, dateFormat);
//            vm.report.investigationDate = vm.investigationDate;
//            vm.report.engine.new_date = vm.report.engine.new_date.toLocaleString();
//            vm.report.workBegin = vm.workBegin;
//            vm.report.workEnd = vm.workEnd;

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

        function getTClasses() {
            Passport.getTClasses()
                .then(function(data) {
                    vm.tclasses.all = data;
                });
        }

//        function enterValue(event, param, prop) {
//            event.stopPropagation();
//
//            var promise = $mdEditDialog.small({
//                modelValue: param[prop],
//                placeholder: 'Введите значение',
//                save: function (input) {
//                param[prop] = input.$modelValue;
//            },
//            targetEvent: event,
//            validators: {
//                'md-maxlength': 30,
//                'ng-pattern': '/^[0-9.,]*$/'
//            },
//            messages: {
//                'md-maxlength': 'Слишком большое значение',
//                'required': 'Обязательное значение'
//            }
//            });
//
//            promise.then(function (ctrl) {
//                var input = ctrl.getInput();
//
//                input.$viewChangeListeners.push(function () {
//                input.$setValidity('test', input.$modelValue !== 'test');
//                });
//            });
//        }

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
        }
    }
})();
