(function() {
    'use strict';

    angular
        .module('app.upload.service')
        .factory('UploadService', UploadService);

    UploadService.$inject = ['$http'];
    function UploadService($http) {
        var service = {
            query: query,
            remove: remove
        };

        return service;

        function query() {
            return $http.get('/api/file/').
                then(function(resp) {
                    return resp.data;
                });
        }

        function remove(id) {
            return $http.delete('/api/file/' + id + '/').
                then(function(resp) {
                    return resp.data;
                });
        }
    }
})();
