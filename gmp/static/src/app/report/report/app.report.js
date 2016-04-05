(function() {
    'use strict';

    angular
        .module('app.report')
        .controller('ReportController', ReportController);

    ReportController.$inject = ['$scope', '$state', 'UserData', 'Department', 'Engine', 'Passport', 'Upload'];
    function ReportController($scope, $state, UserData, Department, Engine, Passport, Upload) {

        $scope.upload = upload;

        var vm = this,
            pages = [
                'report/team.tpl.html',
                'report/report_info.tpl.html',
                'measurers.tpl.html',
                'lpu.tpl.html',
                'report/dates.tpl.html',
                'engines.tpl.html',
                'order.tpl.html',
                'report/photos.tpl.html',
//                'values.tpl.html',
//                'docs.tpl.html',
//                'therm.tpl.html',
//                'vibro.tpl.html',
//                'resistance.tpl.html',
//                'signers.tpl.html'
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


        vm.allEmployees = [];
        vm.control_types = control_types;
        vm.createPassport = createPassport;
        vm.engine = engine;
        vm.workBegin = undefined;
        vm.workEnd = undefined;
        vm.lpus = {};
        vm.orgs = {};
        vm.pages = pages;
        vm.procKeyPress = procKeyPress;
        vm.tclasses = {all: [], selected: ''};
        vm.getLPUs = getLPUs;
        vm.measurers = measurers;
        vm.report = {
            team: undefined,
            measurers: measurers.selected,
            files: {},
            therm: {},
            vibro: {},
            order: {},
            resistance: {}
        };
        vm.setSelected = setSelected;

        activate();

        function procKeyPress(data, clickEvent) {
            if (clickEvent.key === 'Enter') {
                data.push(null);
            }
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
            vm.report.info = {
                license: 'Договор №          от          на выполнение работ по экспертизе промышленной безопасности.'
            };
            vm.report.team = {};
            vm.report.docs = [null];
            vm.report.obj_data = {
                detail_info: [null]
            };

            getEmployees();
            getEngines();
            getOrgs();
            getTClasses();
        }

        function createPassport() {
//            console.log('docs ' + JSON.stringify(vm.report.docs));
//            console.log('investigationDate ' + vm.investigationDate.toLocaleString());
//            console.log('begin ' + vm.workBegin);
//            console.log('end ' + vm.workEnd.toLocaleString());
//            Passport.createPassport(vm.workBegin);
            vm.report.type =  'report';
            console.log('team:', JSON.stringify(vm.report));
//            return;
//            console.dir('vm.tclasses.all: ' + JSON.stringify(vm.tclasses.all));
//            vm.report.therm.tclass = vm.tclasses.all.filter(function(el) {
//                return el.name === vm.tclasses.selected;
//            })[0].id;
//            console.dir('selected class: ' + JSON.stringify(vm.report.therm));
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
