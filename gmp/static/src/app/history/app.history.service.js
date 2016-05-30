(function() {
    'use strict';

    angular
        .module('app.report')
        .constant('URL_HISTORY_API', '/api/history_input/')
        .factory('History', History);

    function History($http, URL_HISTORY_API) {
        'ngInject';

        var history = {
            create: create,
            update: update,
            get: get,
            list: list,
            setCurrentModelValue: setCurrentModelValue,
            getCurrentModelValue: getCurrentModelValue,
            clearCurrentModelValue: clearCurrentModelValue,
        };

        return history;

        ////////////////////////////

        var modelValue = undefined;

        function create(data) {
            return $http.post(URL_HISTORY_API, data);
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

        function setCurrentModelValue(value) {
            modelValue = value;
        }

        function getCurrentModelValue() {
            return modelValue;
        }

        function clearCurrentModelValue() {
            modelValue = undefined;
        }
    }
})();
