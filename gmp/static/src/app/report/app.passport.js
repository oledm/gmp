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
            pages = [
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
            ],
            control_types = [
                {
                    name: 'VIK',
                    full_name: 'Визуальный и измерительный контроль'
                },
                {
                    name: 'UK',
                    full_name: 'Ультразвуковой контроль'
                },
                {
                    name: 'TK',
                    full_name: 'Тепловой контроль'
                },
                {
                    name: 'VD',
                    full_name: 'Вибродиагностический контроль'
                },
                {
                    name: 'EK',
                    full_name: 'Электрический контроль'
                }
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
        vm.control_types = control_types;
        vm.createPassport = createPassport;
        vm.engine = engine;
        vm.workBegin = undefined;
        vm.workEnd = undefined;
        vm.investigationDate = undefined;
        vm.lpus = {};
        vm.orgs = {};
        vm.pages = pages;
        vm.tclasses = {all: [], selected: ''};
        vm.getLPUs = getLPUs;
        vm.measurers = measurers;
        vm.ranks = ranks;
        vm.report = {
            team: undefined,
            measurers: measurers.selected,
            files: {},
            therm: {},
            vibro: {},
            order: {},
            resistance: {}
        };
        vm.reportType = {};
        vm.setSelected = setSelected;

        activate();

        //////////////////////////

        if ($state.is('passport')) {
            vm.reportType = {
                'title': 'паспорта двигателя',
                'button': 'паспорт',
                'type': 'passport'
            };
            vm.report.team = [{'name': '', 'required': true}];
            vm.report.docs = docs;
        } else if ($state.is('report')) {
            vm.pages = [
                'team.tpl.html',
                'report_info.tpl.html',
                'measurers.tpl.html',
                'lpu.tpl.html',
//                'dates.tpl.html',
                'engines.tpl.html',
                'order.tpl.html',
//                'values.tpl.html',
//                'docs.tpl.html',
//                'photos.tpl.html',
//                'therm.tpl.html',
//                'vibro.tpl.html',
//                'resistance.tpl.html',
//                'signers.tpl.html'
            ];
            vm.report.info = {
                license: 'Договор №          от          на выполнение работ по экспертизе промышленной безопасности.'
            };
            vm.reportType = {
                'title': 'экспертного заключения',
                'button': 'заключение',
                'type': 'report'
            };
            vm.report.team = {};
            vm.report.docs = [null];
        }

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
            vm.report.type = vm.reportType.type;
            console.log('team:', JSON.stringify(vm.report));
            return;
            delete vm.report.team[0].required;
            console.dir('vm.tclasses.all: ' + JSON.stringify(vm.tclasses.all));
            vm.report.therm.tclass = vm.tclasses.all.filter(function(el) {
                return el.name === vm.tclasses.selected;
            })[0].id;
            console.dir('selected class: ' + JSON.stringify(vm.report.therm));
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

        function setSelected(selected, item) {
            var id = item.id,
                index = selected.indexOf(id);
            if (index !== -1) {
                selected.splice(index, 1);
                item.selected = false;
            } else {
                item.selected = true;
                selected.push(id);
            }
        }
    }
})();
