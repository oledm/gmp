(function() {
    'use strict';

    angular
        .module('app.report')
        .filter('searchIdInObject', SearchIdInObject)
        .controller('ContainerController', ContainerController);

    function SearchIdInObject() {
        return function(inputArr, matchArr) {
            let matchIds = [], output = [];
            angular.forEach(matchArr, function(value) {
                matchIds.push(value.id);
            });

            angular.forEach(inputArr, function(value) {
                if (matchIds.indexOf(value.id) !== -1) {
                    output.push(value);
                }
            });
            return output;
        }
    }

    function ContainerController($state, $stateParams, ServerData, orgs, allEmployees, allDevices, measurers, History, localStorageService) 
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
                'container/devices.tpl.html',
                'container/report_info.tpl.html',
                'container/order.tpl.html',
                'container/team.tpl.html',
                'measurers.tpl.html',
                'container/schemes.tpl.html',
                'container/results.tpl.html',
                'container/licenses.tpl.html',
            ],
            ranks = [
                'руководитель бригады',
                'зам. руководителя бригады',
                'член бригады'
            ],
            reportId = $stateParams.id,
            readOnlyMode = _.isFinite(parseInt(reportId)),
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
                    measures: [],
                    conclusion: 'Минимальные измеренные толщины стенок элементов сосуда,' + 
                                ' находятся в пределах паспортных значений. Недопустимых' + 
                                ' утонений стенок основных элементов сосуда в зонах ' + 
                                'контроля не обнаружено.'
                },
                UK: {
                    measures: [],
                    conclusion: 'Недопустимых дефектов в сварных соединениях и в ' + 
                                'околошовных зонах не обнаружено.'
                },
                T: {
                    values: [],
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


        vm.addEmployee = addEmployee;
        vm.addToCollection = addToCollection;
        vm.addUTPoint = addUTPoint;
        vm.allEmployees = allEmployees;
        vm.checkElementName = checkElementName;
        vm.control_types = control_types;
        vm.device_conditions = device_conditions;
        vm.createPassport = createPassport;
        vm.devices = devices;
        vm.orgs = orgs;
        vm.pages = pages;
        vm.procKeyPress = procKeyPress;
        vm.getLPUs = getLPUs;
        vm.report = {
            files: {},
            info: info,
            schemes: schemes,
            measurers: {all: measurers, selected: []},
            lpus: [],
            results: results,
            url: 'report-container',
            team: {
                spec: {},
                all: [{'id': '', 'required': true}]
            },
            order: {},
        };

//        vm.uuid = uuid.v4();
        vm.ranks = ranks;
        vm.removeEmployee = removeEmployee;
        vm.report_initial_state = angular.copy(vm.report)
        vm.restore_initial_state = restore_initial_state; 
        vm.setSelected = setSelected;
        vm.reportId = reportId;

        activate(); 

        ///////////////////////////////////////////////////

        function restore_initial_state() {
            localStorageService.remove('model');
            angular.copy(vm.report_initial_state, vm.report);
            $state.go($state.current, {}, {reload: true});
        }

        function addEmployee() {
//            newUUID();
            vm.report.team.all.push({
                'id': '', 'required': false
            });
        }

        function activate() {
            var modeldata = History.getCurrentModelValue();
            if(angular.isDefined(modeldata)) {
                angular.copy(modeldata, vm.report);
                History.clearCurrentModelValue();
            }
        }

        function showError(msg, title='Ошибка!') {
            let message = `
<div class="alert alert-danger alert-dismissible" role="alert">
<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>
<strong>${title}</strong> ${msg}
</div>
            `
            let angularMessage = angular.element(message);
            angular.element(document).find('#messageBox').append(angularMessage);
        }

        function createPassport() {
//            console.log('report:', JSON.stringify(vm.report));
            let lead = vm.report.team.all.filter(m => m.rank === 'руководитель бригады');
            if (lead.length === 0) {
                showError('Не выбран руководитель бригады')
            } else {
                History.saveIfExist(vm.report);

                ServerData.report({'report_data': vm.report})
                    .$promise.then(null,
                        data => showError('Отчет не создан. Обратитесь за помощью к разработчику'));
            }
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

        function removeEmployee(index) {
            if (vm.report.team.all.length > 1) {
                vm.report.team.all.splice(index, 1);
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

            if (!readOnlyMode) {
                History.save(vm.report);
            }
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

        function addUTPoint(measure) {
            var item = undefined;
            if (measure.title.toLowerCase().search(/днище/i) !== -1) {
                item = {'passport': vm.report.device.dimensions_side_bottom, 'real': null};
            } else if (measure.title.toLowerCase().search(/обечайка/i) !== -1) {
                item = {'passport': vm.report.device.dimensions_side_ring, 'real': null};
            } else {
                item = {'passport': null, 'real': null};
            }
            measure.data.push(item);
        }

        function checkElementName(value) {
            var name = value.element;
            if (name.search(/днище/i) !== -1) {
                value.width = vm.report.device.dimensions_side_bottom;
            } else if (name.search(/обечайка/i) !== -1) {
                value.width = vm.report.device.dimensions_side_ring;
            }
        }
    }
})();
