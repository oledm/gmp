(function() {
    'use strict';

    angular
        .module('app.report')
        .directive('saveHistory', SaveHistory);

    function SaveHistory(History, $timeout) {
        'ngInject';

        return {
            scope: {
                model: '=saveHistory'
            },
            link: function(scope, elem, attrs) {
                var timeout = undefined,
                    history_id = undefined,
                    secondsWaitForModelChange = 2;

                scope.$watch(
                    () => scope.model,
                    (newVal, oldVal) => {
//                        console.log('val: ' + JSON.stringify(newVal));
                        if (newVal !== oldVal) {
                            updateHistory(newVal);
                        }
                    },
                    true
                );

                loadHistory(175);

                function updateHistory(newVal) {
                    if (timeout) {
                        $timeout.cancel(timeout);
                    }
                    timeout = $timeout(() => {
//                        console.log('write new model to DB');
                        if (!history_id) {
                            History.create({obj_model: newVal})
                                .then(response => history_id = response.data.id);
                        } else {
                            History.update(history_id, {obj_model: newVal});
                        }
                    }, secondsWaitForModelChange * 1000);
                }

                function loadHistory(id) {
                    History.get(id)
                        .then(response => {
                            angular.copy(response.data.obj_model, scope.model);
                        });
                }
            }
        }
    }
})();
