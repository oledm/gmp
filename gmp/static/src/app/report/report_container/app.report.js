(function() {
    'use strict';

    angular
        .module('app.report')
        .controller('ReportContainerController', ReportContainerController)
        .directive("contenteditable", function() {
	  return {
	    restrict: "A",
	    require: "ngModel",
	    link: function(scope, element, attrs, ngModel) {

	      function read() {
		ngModel.$setViewValue(element.html());
	      }

	      ngModel.$render = function() {
		element.html(ngModel.$viewValue || "");
	      };

	      element.bind("blur keypress change", function() {
		scope.$apply(read);
		scope.$apply();
	      });
	    }
	};
    });

    function ReportContainerController($scope, Passport, Upload, ServerData) {
        'ngInject';

        $scope.upload = upload;

        var vm = this,
            pages = [
                'report_container/devices.tpl.html',
                'report_container/report_info.tpl.html',
                'report_container/order.tpl.html',
                'report_container/team2.tpl.html',
                'measurers.tpl.html',
                'report_container/signers.tpl.html',
                'report_container/schemes.tpl.html',
                'report_container/results.tpl.html',
//                'report_container/team.tpl.html',
//                'report/team.tpl.html',
//                'report_container/results.tpl.html',
//                'report_container/device_location.tpl.html',
//                'report/dates.tpl.html',
//                'engines.tpl.html',
//                'report/photos.tpl.html',
//                'values.tpl.html',
//                'docs.tpl.html',
//                'therm.tpl.html',
//                'vibro.tpl.html',
//                'resistance.tpl.html',
            ],
            control_types = [
                {
                    chapter: 'Визуальный и измерительный контроль',
                    name: 'ВИК',
                    full_name: 'Визуальный и измерительный контроль'
                },
                {
                    chapter: 'Ультразвуковая толщинометрия элементов сосуда',
                    name: 'УК',
                    full_name: 'Ультразвуковой контроль'
                },
                {
                    chapter: 'Ультразвуковой контроль качества сварных соединений',
                    name: 'УК',
                    full_name: 'Ультразвуковой контроль'
                },
                {
                    chapter: 'Контроль физико-механических свойств (твёрдости) ' + 
                        'сварных соединений и основного металла',
                    name: 'ВИК',
                    full_name: 'Визуальный и измерительный контроль'
                },
                {
                    chapter: 'Магнитопорошковый контроль сварных соединений и основного металла',
                    name: 'МК',
                    full_name: 'Магнитопорошковый контроль'
                },
            ],
            devices = {
                all: ServerData.query({category: 'container'}),
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
            ],
            measurers = {
                all: ServerData.measurers(),
                selected: [],
                sortOrder: 'name'
            },
            results = {
                VIK: {
                    results: [
                        {value: 'Сосуд расположен на стальной опоре юбочного типа. ' +
                            'Состояние опорной конструкции и анкерных болтов крепления ' +
                            'юбочной опоры к стальной раме – удовлетворительное.'},
                        {value: 'Корпус сосуда (обечайка, днища) видимых формоизменений (нарушений) ' +
                            'геометрических размеров и недопустимых деформаций не имеет.'
                        },
                        {value: 'Основной металл корпуса сосуда (обечайка, днища) видимых трещин, ' +
                            'вмятин, выпучин, коррозионных повреждений и других дефектов, ' +
                            'вызванных условиями эксплуатации, не имеет.'
                        },
                        {value: 'Сварные соединения в удовлетворительном состоянии. Видимых ' +
                            'дефектов (поверхностных трещин всех видов и направлений, пор, подрезов, ' +
                            'свищей и др.) не обнаружено.'
                        },
                        {value: 'Места вварки штуцеров в корпус сосуда находятся в удовлетворительном состоянии. ' +
                            'Состояние штуцеров, фланцев и крепежных элементов – удовлетворительное.'
                        },
                        {value: 'Максимальная измеренная овальность обечайки не превышает допустимого ' +
                            'значения 1,0% определённого п.4.2.3. ПБ 03-584-03 и составляет – 0,1%.'
                        },
                        {value: 'Состояние наружного защитного лакокрасочного покрытия ' +
                            'корпуса сосуда – удовлетворительное.'
                        }
                    ],
                    conclusion: 'Недопустимых дефектов и формоизменений элементов сосуда, влияющих ' +
                        'на его дальнейшую безопасную эксплуатацию, не выявлено.'
                },
                UT: {
                    common: [],
                    top_bottom: [],
                    ring: [],
                    bottom_bottom: [],
                    top_cap: [],
                    bottom_cap: [],
                    results: [
                        {value: 'Минимальная измеренная толщина стенки верхнего днища –' + 
                                '   мм, скорость коррозии составляет  мм/год'
                        },
                        {value: 'Минимальная измеренная толщина стенки обечайки –' + 
                                '   мм, скорость коррозии составляет  мм/год'
                        },
                        {value: 'Минимальная измеренная толщина стенки нижнего днища –' + 
                                '   мм, скорость коррозии составляет  мм/год'
                        },
                    ],
                    conclusion: 'Минимальные измеренные толщины стенок элементов сосуда,' + 
                                ' находятся в пределах паспортных значений. Недопустимых' + 
                                ' утонений стенок основных элементов сосуда в зонах ' + 
                                'контроля не обнаружено.'
                },
                UK: {
                    top_bottom: [
                        {'site': 'К1'},
                        {'site': 'К2'},
                    ],
                    ring: [
                        {'site': 'П1'},
                        {'site': 'К3'},
                    ],
                    bottom_bottom: [
                        {'site': 'К4'},
                    ],
//                    results: [
//                        {value: 'Первый результат'},
//                        {value: 'Второй результат'},
//                    ],
                    conclusion: 'Недопустимых дефектов в сварных соединениях и в ' + 
                                'околошовных зонах не обнаружено.'
                },
            };


        vm.addToCollection = addToCollection;
        vm.allEmployees = ServerData.users();
        vm.control_types = control_types;
        vm.device_conditions = device_conditions;
        vm.createPassport = createPassport;
        vm.devices = devices;
        vm.lpus = {};
        vm.orgs = {};
        vm.pages = pages;
        vm.procKeyPress = procKeyPress;
        vm.getLPUs = getLPUs;
        vm.measurers = measurers;
        vm.report = {
            team: {},
            files: {
                'legend': [],
                'conrtol_VIK': [],
                'conrtol_UK_container': [],
                'conrtol_UK_connections': [],
                'conrtol_magnit': [],
            },
            info: {
                'license': 'Договор субподряда между ООО «ГАЗМАШПРОЕКТ» и ООО «Стройгазмонтаж»',
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
                'license_more': ''
            },
            schemes: {
                'VIK': 'Схема проведения визуально-измерительного контроля сосуда',
                'UK_container': 'Схема проведения ультразвуковой толщинометрии и твердометрии сосуда',
                'UK_connections': 'Схема проведения ультразвукового контроля сварных соединений сосуда',
                'magnit': 'Схема проведения магнитопорошкового контроля сосуда',
            },
            measurers: measurers.selected,
            results: results,
        };
//            team: undefined,
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
            getOrgs();
        }

        function addToCollection(arr, value) {
            var value = value.trim();
            // Test for absence of a new value in array 
            if (value !== '' && arr.indexOf(value) === -1 ) {
                arr.push({'value': value});
            }
        }

        function createPassport() {
////            console.log('docs ' + JSON.stringify(vm.report.docs));
////            console.log('investigationDate ' + vm.investigationDate.toLocaleString());
            vm.report.type = 'report-container';
            console.log('report:', JSON.stringify(vm.report));
////            console.dir('selected class: ' + JSON.stringify(vm.report.therm));
            Passport.createPassport(vm.report);
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

        function procKeyPress(clickEvent, arr) {
            // Check for Return (Enter) key pressed
            if (clickEvent.which === 13) {
                clickEvent.preventDefault();
                addToCollection(arr, clickEvent.target.value);
                clickEvent.target.value = '';
            }
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
