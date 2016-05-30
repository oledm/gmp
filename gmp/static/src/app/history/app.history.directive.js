(function() {
    'use strict';

    angular
        .module('app.report')
        .directive('saveHistory', SaveHistory);

    function SaveHistory(History, $timeout, moment, $compile, $state) {
        'ngInject';

        return {
            scope: {
                model: '=saveHistory',
                reportId: '@'
            },
            controller: function($scope) {
                var ctrl = this;

                ctrl.createNewReport = createNewReport;

                function createNewReport() {
                    History.setCurrentModelValue($scope.model)
                    $state.go('report-container', {id: undefined});
                }
            },
            controllerAs: 'ctrl',
            link: function(scope, elem, attrs) {
                var timeout = undefined,
                    history_id = undefined,
                    oldVal = undefined,
                    secondsWaitForModelChange = 2;

                // Deep watch for changes in every in-object's properties
//                scope.$watch(
//                    () => scope.model,
//                    (newVal, oldVal) => {
////                        console.log('old val: ' + JSON.stringify(oldVal));
////                        console.log('new val: ' + JSON.stringify(newVal));
//                        if (newVal !== oldVal) {
//                            updateHistory(newVal);
//                        }
//                    },
//                    true
//                );

                activate(scope.reportId);
                //////////////////////////////////////////////////

                function activate(id) {
                    var id = parseInt(id);
                    if(!_.isFinite(id)) {
                        // History id not provided. New report mode
                        console.log('addListener');
                        addChangeListener();
                    } else {
                        // Load history data into model
                        loadHistory(id);
                        showReadOnlyWarning();
                    }
                }

                function addChangeListener() {
                    elem.on('change', () => {
                        console.log(`Form changes. Wait ${secondsWaitForModelChange} seconds before saving`);
                        angular.copy(scope.model, oldVal);
                        updateHistory(scope.model);
                    });
                }

                function loadHistory(id) {
                    History.get(id)
                        .then(history_data => {
                            if (history_data.hasOwnProperty('obj_model')) {
                                let data = history_data.obj_model;
                                // Deep search model object and convert all datetime
                                // string values to Date instance for correct display
                                // by date-picker widget.
                                fromStringToDate(data);
                                angular.copy(data, scope.model);
                            }
                        });
                }

                function showReadOnlyWarning() {
                    var msg = 
                    `
                    <div class="alert alert-warning" role="alert">
                    <strong>Внимание!</strong><span> Вы находитесь в режиме просмотра истории. Все внесенные изменения не будут сохранены. Вы можете создать новую форму отчета с такими же исходными данными.</span>
                    <div class="block text-center alert__button">
                        <button ng-click="ctrl.createNewReport()" class="btn btn-primary"> Создать </button>    
                    </div>
                    `;
                    
                    elem.prepend($compile(msg)(scope));
                }

                function updateHistory(newVal) {
                    clearTimeout();

                    timeout = $timeout(() => {
//                        console.log('write new model to DB');
                        if (!history_id) {
                            console.log('Write history:', newVal);
                            History.create({obj_model: newVal})
                                .then(response => history_id = response.data.id);
                        } else {
                            console.log('History update', newVal);
                            History.update(history_id, {obj_model: newVal});
                        }
                    }, secondsWaitForModelChange * 1000);
                }

                function fromStringToDate(data) {
                    for (let prop in data) {
                        if (data.hasOwnProperty(prop)) {
                            let item = data[prop];
                            if (angular.isString(item)) {
                                let dateOnly = item.split('T')[0];
                                if (moment(dateOnly, 'YYYY-MM-DD', true).isValid()) {
//                                    console.log(`${prop}:`, item, '-->', JSON.stringify(date));
                                    data[prop] = new Date(item);
                                }
                            } else {
                                fromStringToDate(item);
                            }
                        }
                    }
                }

                function clearTimeout() {
                    if (timeout) {
                        $timeout.cancel(timeout);
                    }
                }
            }
        }
    }
})();
