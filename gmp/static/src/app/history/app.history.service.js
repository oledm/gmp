(function() {
    'use strict';

    angular
        .module('app.report')
        .constant('URL_HISTORY_API', '/api/history_input/')
        .factory('History', History);

    function History($http, $timeout, URL_HISTORY_API) {
        'ngInject';

        var history = {
            get: get,
            list: list,
            save: save,
            saveIfExist: saveIfExist,
            saveNow: saveNow,
            setCurrentModelValue: setCurrentModelValue,
            getCurrentModelValue: getCurrentModelValue,
            clearCurrentModelValue: clearCurrentModelValue,
            clearHistoryId: clearHistoryId,
        };

        const secondsWaitForModelChange = 2;

        return history;

        ////////////////////////////

        var history_id = undefined,
            timeout = undefined,
            modelValue = undefined;


        function create(data) {
            return $http.post(URL_HISTORY_API, data);
        }

        function clearTimeout() {
            if (timeout) {
                $timeout.cancel(timeout);
            }
        }

        function get(id) {
            if (angular.isDefined(id) && angular.isNumber(id)) {
                return $http.get(`${URL_HISTORY_API}${id}/`)
                    .then(response => response.data);
            } else {
                console.warn('Неверно указан id для выполнения запроса History.get:',
                             `${URL_HISTORY_API}<id>/`,
                             `(получено значение ${id})`);
                return undefined;
            }
        }

        function list() {
            return $http.get(`${URL_HISTORY_API}`)
                .then(response => response.data);
        }

        function update(id, data) {
            if (angular.isDefined(id) && angular.isNumber(id)) {
                return $http.put(`${URL_HISTORY_API}${id}/`, data);
            } else {
                console.warn('Неверно указан id для выполнения запроса History.update:',
                             `${URL_HISTORY_API}<id>/`,
                             `(получено значение ${id})`);
                return undefined;
            }
        }

        function save(data) {
            clearTimeout();
//            console.log(`Model changes. Wait ${secondsWaitForModelChange} seconds before saving`);

            timeout = $timeout(() => {
                saveNow(data);
            }, secondsWaitForModelChange * 1000);
        }

        function saveIfExist(data) {
            if (history_id) {
                console.log('history_id is', history_id);
                update(history_id, {obj_model: data});
            }
        }

        function saveNow(data) {
            if (!history_id) {
//                console.log('Write history:', data);
                create({obj_model: data})
                    .then(response => history_id = response.data.id);
            } else {
//                console.log('History update', data);
                update(history_id, {obj_model: data});
            }
        }

        function setCurrentModelValue(value) {
            modelValue = value;
            clearHistoryId();
        }

        function clearHistoryId() {
            history_id = undefined;
        }

        function getCurrentModelValue() {
            return modelValue;
        }

        function clearCurrentModelValue() {
            modelValue = undefined;
        }
    }
})();
