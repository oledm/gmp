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
            list: list
        };

        return history;

        ////////////////////////////

        function create(data) {
            return $http.post(URL_HISTORY_API, data);
        }

        function update(id, data) {
            return $http.put(`${URL_HISTORY_API}${id}/`, data);
        }

        function get(id) {
            return $http.get(`${URL_HISTORY_API}${id}/`);
        }

        function list() {
            return $http.get(`${URL_HISTORY_API}`)
                .then(response => response.data);
        }
    }
})();
