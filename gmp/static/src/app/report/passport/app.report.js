(function() {
    'use strict';

    angular
        .module('app.report')
        .controller('PassportController', PassportController);

//    function Passportengine($scope, $state, UserData, Department, Engine, Passport, Upload) {
    function PassportController($state, $stateParams, ServerData, orgs, allTClasses,
                    allEmployees, allDevices, measurers, History, localStorageService) {
        'ngInject';

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
                'passport/team.tpl.html',
                'measurers.tpl.html',
                'lpu.tpl.html',
                'passport/dates.tpl.html',
                'engines.tpl.html',
                'passport/values.tpl.html',
                'passport/docs.tpl.html',
                'passport/photos.tpl.html',
                'therm.tpl.html',
                'vibro.tpl.html',
                'resistance.tpl.html',
                'passport/signers.tpl.html'
            ],
            ranks = [
                'руководитель бригады',
                'зам. руководителя бригады',
                'член бригады'
            ],
            engine = {
                all: allDevices,
                selected: {
                    'type': '',
                    'serial_number': 0
                },
                sortOrder: 'name'
            };


        vm.addEmployee = addEmployee;
        vm.allEmployees = allEmployees;
        vm.createPassport = createPassport;
        vm.engine = engine;
        vm.workBegin = undefined;
        vm.workEnd = undefined;
        vm.investigationDate = undefined;
        vm.orgs = orgs;
        vm.pages = pages;
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
            type: $state.current.data.type,
            docs: docs,
            resistance: {}
        };
        vm.reportId = $stateParams.id;
        vm.report_initial_state = angular.copy(vm.report)
        vm.restore_initial_state = restore_initial_state; 
        vm.setSelected = setSelected;

        activate();

        function activate() {
            var modeldata = History.getCurrentModelValue();
            if(angular.isDefined(modeldata)) {
                angular.copy(modeldata, vm.report);
                History.clearCurrentModelValue();
            }
        }

        function addEmployee() {
            vm.report.team.push({
                'id': '', 'required': false
            });
        }

//        function createPassport() {
//            console.log('report:', JSON.stringify(vm.report));
//            delete vm.report.team[0].required;
////            console.dir('vm.tclasses.all: ' + JSON.stringify(vm.tclasses.all));
//            vm.report.therm.tclass = vm.tclasses.all.filter(function(el) {
//                return el.name === vm.tclasses.selected;
//            })[0].id;
////            console.dir('selected class: ' + JSON.stringify(vm.report.therm));
//            Passport.createPassport(vm.report);
//        }

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
            console.log('report:', JSON.stringify(vm.report));
            History.saveNow(vm.report);
            ServerData.report({'report_data': vm.report})
                .$promise.then(null,
                    data => showError('Паспорт не создан. Обратитесь за помощью к разработчику'));
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
    }
})();
