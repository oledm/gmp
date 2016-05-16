(function() {
    'use strict';

    angular
        .module('app.report')
        .factory('History', History);

    function History($http) {
        'ngInject';

        var history = {
            create: create,
            update: update
        };

        return history;

        ////////////////////////////

        function create(data) {
            return $http.post('/api/history_input/', data);
        }

        function update(id, data) {
            return $http.put(`/api/history_input/${id}/`, data);
        }
    }
})();
