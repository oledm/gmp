(function() {
    'use strict';

    angular
        .module('app.report')
        .controller('ReportContainerController', ReportContainerController);

    function ReportContainerController($scope, UserData, Department, Passport, Upload, ServerData) {
        'ngInject';

        $scope.upload = upload;

        var vm = this,
            pages = [
                'report_container/devices.tpl.html',
                'report_container/report_info.tpl.html',
                'report_container/order.tpl.html',
                'report_container/team.tpl.html',
                'report_container/signers.tpl.html',
                'report_container/schemes.tpl.html',
//                'report_container/device_location.tpl.html',
//                'measurers.tpl.html',
//                'report/dates.tpl.html',
//                'engines.tpl.html',
//                'report/photos.tpl.html',
//                'values.tpl.html',
//                'docs.tpl.html',
//                'therm.tpl.html',
//                'vibro.tpl.html',
//                'resistance.tpl.html',
            ],
            measurers = {
                all: Department.measurers(),
                selected: [],
                sortOrder: 'name'
            },
            devices = {
                all: [],
//                selected: {
//                    'type': '',
//                    'serial_number': 0
//                },
//                sortOrder: 'name'
            },
            device_conditions = [
                'работоспособное',
                'неработоспособное',
                'предельное'
            ];


//        vm.addToCollection = addToCollection;
        vm.allEmployees = [];
//        vm.control_types = control_types;
        vm.device_conditions = device_conditions;
        vm.createPassport = createPassport;
        vm.devices = devices;
//        vm.workBegin = undefined;
//        vm.workEnd = undefined;
        vm.lpus = {};
        vm.orgs = {};
        vm.pages = pages;
//        vm.procKeyPress = procKeyPress;
//        vm.tclasses = {all: [], selected: ''};
        vm.getLPUs = getLPUs;
//        vm.measurers = measurers;
        vm.report = {
            team: [],
            files: {
                'legend': [],
                'conrtol_VIK': [],
                'conrtol_UK_container': [],
                'conrtol_UK_connections': [],
                'conrtol_magnit': [],
            },
            info: {
                'info_investigation': 'Экспертиза промышленной безопасности проводится впервые. ' +
                    '\nНО, ВО – 1 раз в 2 года (ответственный за осуществление ' + 
                    'производственного контроля за эксплуатацией сосуда). ' +
                    '\nНО, ВО – 1 раз в 4 года (уполномоченная специализированная организация, ' +
                    'ответственный за осуществление производственного контроля за эксплуатацией сосуда). ' +
                    '\nГИ – 1 раз в 8 лет (уполномоченная специализированная организация, ' + 
                    'ответственный за осуществление производственного контроля за эксплуатацией сосуда)',
                'info_repair': 'В представленной технической документации не отмечено',
                'danger_places': 'Места концентраций напряжений – продольные и кольцевые сварные швы, ' + 
                    'места вварки штуцеров; места наиболее вероятного коррозионного износа – ' + 
                    'внутренняя поверхность нижнего днища',
            },
            schemes: {
                'VIK': 'Схема проведения визуально-измерительного контроля сосуда',
                'UK_container': 'Схема проведения ультразвуковой толщинометрии и твердометрии сосуда',
                'UK_connections': 'Схема проведения ультразвукового контроля сварных соединений сосуда',
                'magnit': 'Схема проведения магнитопорошкового контроля сосуда',
            },
        };
//            team: undefined,
//            measurers: measurers.selected,
//            files: {
//                'main': [],
//                'therm1': [],
//                'therm2': [],
//                'licenses': []
//            },
//            therm: {},
//            vibro: {},
//            order: {},
//            resistance: {}
//        };
        vm.setSelected = setSelected;

        activate();

        function activate() {
            getContainers();
            getOrgs();
            getEmployees();
//            vm.report.info = {
//                license: 'Договор №          от          на выполнение работ по экспертизе промышленной безопасности.'
//            };
//            vm.report.team = {};
//            vm.report.docs = [];
//            vm.report.obj_data = {
//                detail_info: []
//            };
//
//            getEngines();
//            getTClasses();
        }

        function addToCollection(arr, value) {
            var value = value.trim();
            // Test for absence of a new value in array 
            if (value !== '' && arr.indexOf(value) === -1 ) {
                arr.push(value);
            }
        }

        function createPassport() {
////            console.log('docs ' + JSON.stringify(vm.report.docs));
////            console.log('investigationDate ' + vm.investigationDate.toLocaleString());
////            console.log('begin ' + vm.workBegin);
////            console.log('end ' + vm.workEnd.toLocaleString());
////            Passport.createPassport(vm.workBegin);
            vm.report.type = 'report-container';
            console.log('report:', JSON.stringify(vm.report));
////            return;
////            console.dir('vm.tclasses.all: ' + JSON.stringify(vm.tclasses.all));
//            vm.report.therm.tclass = vm.tclasses.all.filter(function(el) {
//                return el.name === vm.tclasses.selected;
//            })[0].id;
////            console.dir('selected class: ' + JSON.stringify(vm.report.therm));
//            Passport.createPassport(vm.report);
        }

        function getEmployees() {
            UserData.getAllUsers()
                .then(function(data) {
                    vm.allEmployees = data;
                });
        }

        function getContainers() {
            ServerData.query({category: 'container'}, function(data) {
                vm.devices.all = data;
//                vm.devices.all = data.map(function(el) {
//                    return el;
//                })
            });
        };

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
//
//        function getTClasses() {
//            Passport.getTClasses()
//                .then(function(data) {
//                    vm.tclasses.all = data;
//                });
//        }
//
//        function procKeyPress(clickEvent, arr) {
//            // Check for Return (Enter) key pressed
//            if (clickEvent.which === 13) {
//                clickEvent.preventDefault();
//                addToCollection(arr, clickEvent.target.value);
//                clickEvent.target.value = '';
//            }
//        }

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

        function upload(element) {
            var fieldname = element.name;
            angular.forEach(element.files, function(file) {
                Upload.upload({
                    url: '/api/upload/',
                    data: {fileupload: file}
                }).
                then(function(response) {
                    vm.report.files[fieldname].push(response.data.id);
                    console.log(vm.report.files);
                }, function(response) {
                    console.log('Error status: ' + response.status);
                });
            });
        }
    }
})();
