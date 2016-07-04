(function() {
    'use strict';

    angular
        .module('app.report')
        .controller('EngineController', EngineController);

    function EngineController($state, $stateParams, ServerData, orgs, allTClasses, connection_types,
                    allEmployees, allDevices, measurers, History, localStorageService) {
        'ngInject';

        var vm = this,
            control_types = [
                {
                    name: 'ВИК',
                    full_name: 'Визуальный и измерительный контроль'
                },
                {
                    name: 'УК',
                    full_name: 'Ультразвуковой контроль'
                },
                {
                    name: 'ТК',
                    full_name: 'Тепловой контроль'
                },
                {
                    name: 'ВД',
                    full_name: 'Вибродиагностический контроль'
                },
                {
                    name: 'ЭЛ',
                    full_name: 'Электрический контроль'
                }
            ],
            docs = [
                {name: 'Журнал ремонта электродвигателя', value: true},
                {name: 'Журнал эксплуатации электродвигателя', value: true},
                {name: 'Инструкция по эксплуатации завода-изготовителя', value: true},
                {name: 'Протоколы штатных измерений и испытаний', value: true},
                {name: 'Паспорт завода-изготовителя на взрывозащищенный электродвигатель', value: true},
                {name: 'Схема электроснабжения электродвигателя', value: true}
            ],
            pages = [
                'engine/team.tpl.html',
                'engine/report_info.tpl.html',
                'measurers.tpl.html',
                'engine/lpu.tpl.html',
                'engine/dates.tpl.html',
                'engine/engines.tpl.html',
                'engine/order.tpl.html',
                'engine/values.tpl.html',
                'engine/docs.tpl.html',
                'engine/photos.tpl.html',
                'engine/therm.tpl.html',
                'engine/vibro.tpl.html',
                'engine/resistance.tpl.html',
                'engine/signers.tpl.html'
            ],
            ranks = [
                'руководитель бригады',
                'зам. руководителя бригады',
                'член бригады'
            ],
            report_types = [
                {
                    alias: 'passport',
                    name: 'Паспорт'
                },
                {
                    alias: 'report',
                    name: 'Заключение'
                }
            ],
            engine = {
                all: allDevices,
                selected: {
                    type: '',
                    serial_number: 0
                },
                sortOrder: 'name'
            },
            reportId = $stateParams.id,
            readOnlyMode = _.isFinite(parseInt(reportId));


        vm.addEmployee = addEmployee;
        vm.allEmployees = allEmployees;
        vm.addToCollection = addToCollection;
        vm.connection_types = connection_types;
        vm.control_types = control_types;
        vm.createPassport = createPassport;
        vm.engine = engine;
        vm.workBegin = undefined;
        vm.workEnd = undefined;
        vm.investigationDate = undefined;
        vm.orgs = orgs;
        vm.pages = pages;
        vm.procKeyPress = procKeyPress;
        vm.tclasses = {all: allTClasses, selected: ''};
        vm.getLPUs = getLPUs;
        vm.ranks = ranks;
        vm.report = {
            team: [{'id': '', 'required': true}],
            measurers: {all: measurers, selected: []},
            files: {},
            lpus: [],
            therm: {},
            vibro: {},
            order: {},
            obj_data: {
                detail_info: []
            },
            docs: docs,
            resistance: {},
            type: report_types[0],
            url: 'report-engine',
        };
        vm.removeEmployee = removeEmployee;
        vm.reportId = reportId;
        vm.report_types = report_types;
        vm.reportTypeChange = reportTypeChange;
        vm.report_initial_state = angular.copy(vm.report)
        vm.restore_initial_state = restore_initial_state; 
        vm.setSelected = setSelected;

        activate();

        /////////////////////////////////////////////////////////////////

        function activate() {
            console.log('reportId:', reportId);
            console.log('readOnlyMode:', readOnlyMode);
            var modeldata = History.getCurrentModelValue();
            if(angular.isDefined(modeldata)) {
                angular.copy(modeldata, vm.report);
                History.clearCurrentModelValue();
            }
        }

        function addEmployee() {
            vm.report.team.push({
                'id': '', 'required': true
            });
        }

        function addToCollection(arr, value) {
            var value = value.trim();
            // Test for absence of a new value in array 
            if (value !== '' && arr.indexOf(value) === -1 ) {
                arr.push(value);
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

        function showError(msg, title='Ошибка!') {
            let message = `
<div class="alert alert-danger alert-dismissible" role="alert">
<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>
<strong>${title}</strong> ${msg}
</div>`
            let angularMessage = angular.element(message);
            angular.element(document).find('#messageBox').append(angularMessage);
        }

        function createPassport() {
//            console.log('report:', JSON.stringify(vm.report));
            History.saveIfExist(vm.report);

            var report_create_error = undefined;
            if (vm.report.type.alias === 'passport') {
                report_create_error = 'Паспорт не создан';
            } else if (vm.report.type.alias === 'report') {
                report_create_error = 'Заключение не создано';
            }

            ServerData.report({'report_data': vm.report})
                .$promise.then(null,
                    data => showError(`${report_create_error}. Обратитесь за помощью к разработчику`));
        }

        function removeEmployee(index) {
            if (vm.report.team.length > 1) {
                vm.report.team.splice(index, 1);
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

        function restore_initial_state() {
            localStorageService.remove('model');
            angular.copy(vm.report_initial_state, vm.report);
            $state.go($state.current, {}, {reload: true});
        }

        function reportTypeChange() {
            switch (vm.report.type.alias) {
                case 'passport':
                    vm.report.files = {"main": [], "licenses": [], "therm1": [], "therm2": []};
                    vm.report.team = [{'id': '', 'required': true}];
                    vm.report.docs = docs;
                    break;
                case 'report':
                    vm.report.files = {"main": [], "therm1": [], "therm2": []};
                    vm.report.team = {};
                    vm.report.docs = [];
                    vm.report.info = {
                        license: 'Договор №          от          на выполнение работ по экспертизе промышленной безопасности.'
                    };
                    break;
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
    }
})();
