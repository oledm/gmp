(function() {
    'use strict';

    angular
        .module('app.engine.service')
        .factory('Engine', Engine);

    Engine.$inject = ['$http'];

    function Engine($http) {
        var engine = {
            getAllEngines: getAllEngines
        };

        return engine;

        ////////////////////////

        function getAllEngines() {
            return $http.get('/api/engine/')
                .then(function(response) {
                    return response.data;
                });
        }
    }

})();
