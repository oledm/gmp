(function() {
    'use strict';

    angular
        .module('app.report')
        .config(ReportConfig)
        .controller('FormController', FormController)
        .controller('ReportContainerController', ReportContainerController);

    function ReportConfig($httpProvider) {
        'ngInject';
        $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
    }

    function FormController($scope, $http) {
        'ngInject';

        $scope.submit = function() {
            console.log('submitted ' + $scope.subject);
            var in_data = { subject: $scope.subject };
            $http.post('/contact/', in_data)
                .success(function(out_data) {
                    console.log('out: ' + out_data);
                });
        }
    }

    function ReportContainerController($scope, $state, $stateParams, ServerData, orgs, allEmployees, allDevices, measurers, History) 
    {
        'ngInject';

        var vm = this,
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
            devices = {all: allDevices},
            device_conditions = [
                'работоспособное',
                'неработоспособное',
                'предельное'
            ],
	    info = {
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
            pages = [
                'report_container/devices.tpl.html',
                'report_container/report_info.tpl.html',
                'report_container/order.tpl.html',
                'report_container/team2.tpl.html',
                'measurers.tpl.html',
                'report_container/signers.tpl.html',
                'report_container/schemes.tpl.html',
                'report_container/results.tpl.html',
                'report_container/licenses.tpl.html',
            ],
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
                HYDRA: {
                    conclusion: 'Проведено гидравлическое испытание сосуда, пробным давлением ' +
                        '1,25 х Р раб. При осмотре элементов сосуда течей, трещин, слезок, потения ' +
                        'в сварных соединениях и на основном металле, течей в разъемных соединениях, ' + 
                        'а также видимых остаточных деформаций и падения давления по манометрам не обнаружено.' 
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
            },
	    schemes = {
                'VIK': 'Схема проведения визуально-измерительного контроля сосуда',
                'UK_container': 'Схема проведения ультразвуковой толщинометрии и твердометрии сосуда',
                'UK_connections': 'Схема проведения ультразвукового контроля сварных соединений сосуда',
                'magnit': 'Схема проведения магнитопорошкового контроля сосуда',
            };


            
	vm.movies = [
            "Lord of the Rings",
            "Drive",
            "Science of Sleep",
            "Back to the Future",
            "Oldboy"
        ];
        vm.yourchoice = '';


        vm.addToCollection = addToCollection;
        vm.allEmployees = allEmployees;
        vm.control_types = control_types;
        vm.device_conditions = device_conditions;
        vm.createPassport = createPassport;
        vm.devices = devices;
        vm.orgs = orgs;
        vm.pages = pages;
        vm.procKeyPress = procKeyPress;
        vm.getLPUs = getLPUs;
//        vm.measurers = {all: measurers, selected: []};
        vm.report = {
            team: {},
            files: {},
            info: info,
            schemes: schemes,
            measurers: {all: measurers, selected: []},
            lpus: [],
            results: results,
            type: $state.current.data.type,
            order: {},
        };

        vm.report_initial_state = angular.copy(vm.report)
        vm.restore_initial_state = restore_initial_state; 
        vm.setSelected = setSelected;
        vm.reportId = $stateParams.id;

        activate(); 

        ///////////////////////////////////////////////////

        function restore_initial_state() {
            angular.copy(vm.report_initial_state, vm.report);
        }

        function activate() {
            var modeldata = History.getCurrentModelValue();
            if(angular.isDefined(modeldata)) {
                angular.copy(modeldata, vm.report);
                History.clearCurrentModelValue();
            }
        }

        function createPassport() {
            console.log('report:', JSON.stringify(vm.report));
            History.saveNow(vm.report);
            ServerData.report({'report_data': vm.report});
        }

        function getLPUs(org) {
            if (angular.isDefined(org)) {
                vm.report.lpus = ServerData.query({
                    category: 'organization',
                    categoryId: org.id,
                    subcategory: 'lpu'});
            }
        }

        ///////////////////////////////////////////////////////////////////////
        // TODO create directive for reusing this funcs
        ///////////////////////////////////////////////////////////////////////
        function addToCollection(arr, value) {
            var value = value.trim();
            // Test for absence of a new value in array 
            if (value !== '' && arr.indexOf(value) === -1 ) {
                arr.push({'value': value});
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
            History.save(vm.report);
        }

        function procKeyPress(clickEvent, arr) {
            // Check for Return (Enter) key pressed
            if (clickEvent.which === 13) {
                clickEvent.preventDefault();
                addToCollection(arr, clickEvent.target.value);
                clickEvent.target.value = '';
            }
        }
        ///////////////////////////////////////////////////////////////////////
        ///////////////////////////////////////////////////////////////////////
        ///////////////////////////////////////////////////////////////////////
    }
})();
