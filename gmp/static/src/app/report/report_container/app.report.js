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
                T: {
                    values: [
                        {
                            element: 'Днище верхнее',
                            point: '1, 2',
                            zone: 'Основной металл',
                            width: '20,0',
                            hardness: '149-166'
                        },
                        {
                            element: 'Обечайка',
                            point: '5, 6',
                            zone: 'Основной металл',
                            width: '20,0',
                            hardness: '149-166'
                        },
                        {
                            element: 'Обечайка',
                            point: '1-4 ,7,8',
                            zone: 'Сварной шов',
                            width: '',
                            hardness: '190-204'
                        },
                        {
                            element: 'Днище нижнее',
                            point: '1, 2',
                            zone: 'Основной металл',
                            width: '20,0',
                            hardness: '143-164'
                        },
                        {
                            element: 'Вход газа',
                            point: '1',
                            zone: 'Основной металл',
                            width: '',
                            hardness: '147-170'
                        },
                        {
                            element: 'Выход газа',
                            point: '1',
                            zone: 'Основной металл',
                            width: '',
                            hardness: '145-158'
                        },
                        {
                            element: 'Люк верхний',
                            point: '1',
                            zone: 'Основной металл',
                            width: '',
                            hardness: '150-168'
                        },
                        {
                            element: 'Люк нижний',
                            point: '1',
                            zone: 'Основной металл',
                            width: '',
                            hardness: '153-169'
                        },
                        {
                            element: 'Патрубок дренажа',
                            point: '1',
                            zone: 'Основной металл',
                            width: '',
                            hardness: '150-170'
                        },
                    ],
                    results: [
                        {value: 'Средняя фактическая твердость основного металла ' + 
                            'контролируемых элементов сосуда, находится в пределах ' + 
                            '143÷170 НВ и не выходит за границы допустимых значений ' + 
                            'твердости контролируемой марки стали. Согласно таблице 8.6 ' + 
                            'СТО Газпром 2-2.3-491-2010 допускаемая твердость находится в ' + 
                            'пределах 120÷180 HB для стали 09Г2С.'
                        },
                        {value: 'Средняя фактическая твердость сварных соединений сосуда, ' + 
                            'находится в пределах 190÷204 НВ и не выходит за границы ' + 
                            'допустимых значений твердости 225 HB (согласно таблице 8.6 ' + 
                            'СТО Газпром 2-2.3-491-2010) для контролируемой марки стали.'
                        },
                    ],
                    conclusion: 'По результатам замеров твердости основного металла и ' + 
                        'сварных соединений сосуда, недопустимых значений не установлено.'
                },
                MK: {
                    values: [
                        {
                            element: 'Кольцевой шов приварки обечайки к верхнему днищу',
                            point: 'МК1',
                            zone: '-',
                            defect: 'ДНО',
                            summary: 'Годен'
                        },
                        {
                            element: 'Кольцевой шов приварки патрубка люка верхнего',
                            point: 'МК2',
                            zone: '-',
                            defect: 'ДНО',
                            summary: 'Годен'
                        },
                        {
                            element: 'Сопряжение швов',
                            point: 'МК3',
                            zone: '-',
                            defect: 'ДНО',
                            summary: 'Годен'
                        },
                        {
                            element: 'Кольцевой шов приварки патрубка манометра',
                            point: 'МК4',
                            zone: '-',
                            defect: 'ДНО',
                            summary: 'Годен'
                        },
                        {
                            element: 'Кольцевой шов приварки патрубка входа газа',
                            point: 'МК5',
                            zone: '-',
                            defect: 'ДНО',
                            summary: 'Годен'
                        },
                        {
                            element: 'Кольцевой шов приварки патрубка выхода газа',
                            point: 'МК6',
                            zone: '-',
                            defect: 'ДНО',
                            summary: 'Годен'
                        },
                        {
                            element: 'Кольцевой шов приварки патрубка люка нижнего',
                            point: 'МК7',
                            zone: '-',
                            defect: 'ДНО',
                            summary: 'Годен'
                        },
                        {
                            element: 'Сопряжение швов',
                            point: 'МК8',
                            zone: '-',
                            defect: 'ДНО',
                            summary: 'Годен'
                        },
                        {
                            element: 'Кольцевой шов приварки обечайки к нижнему днищу',
                            point: 'МК9',
                            zone: '-',
                            defect: 'ДНО',
                            summary: 'Годен'
                        },
                        {
                            element: 'Кольцевой шов приварки патрубка дренажа',
                            point: 'МК10',
                            zone: '-',
                            defect: 'ДНО',
                            summary: 'Годен'
                        },
                    ],
                    conclusion: 'Недопустимых индикаторных рисунков, указывающих ' +
                        'на наличие недопустимых дефектов, не обнаружено.'
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
                'hydra': [],
                'license': [],
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
