(function() {
    'use strict';

    angular
        .module('app.report')
        .directive('saveHistory', SaveHistory);

    function SaveHistory(History, $timeout, moment) {
        'ngInject';

        return {
            scope: {
                model: '=saveHistory',
                reportId: '@'
            },
            link: function(scope, elem, attrs) {
                var timeout = undefined,
                    history_id = undefined,
                    oldVal = undefined,
                    secondsWaitForModelChange = 2;

                elem.on('change', () => {
                    console.log(`Form changes. Wait ${secondsWaitForModelChange} seconds before saving`);
                    angular.copy(scope.model, oldVal);
                    updateHistory(scope.model);
                });


//                scope.$watch(() => FormController.$dirty, newValue => {
//                    console.log('Form dirty: ' + newValue);
//                });
//                scope.$on('FormReady', event => {
//                    console.log('FormReady received');
//                });
//                scope.$watch(FormController.$name + '.$dirty', newValue => {
//                    console.log('Form dirty: ' + newValue);
//                });

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

                loadHistory(scope.reportId);
                //////////////////////////////////////////////////

                function updateHistory(newVal) {
                    if (timeout) {
                        $timeout.cancel(timeout);
                    }
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

                function loadHistory(id) {
                    id = parseInt(id);
                    if(!isFinite(id)) {
                        return;
                    }
//                    console.log('Load history ' + JSON.stringify(id));

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
            }
        }
    }
})();
