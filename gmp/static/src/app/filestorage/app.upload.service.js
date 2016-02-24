(function() {
    'use strict';

    angular
        .module('app.upload.service')
        .factory('UploadService', UploadService);

    UploadService.$inject = ['$http'];
    function UploadService($http) {
        var service = {
            getFiles: getFiles
        };

        return service;

        function getFiles() {
            return $http.get('/api/file/').
                then(function(resp) {
                    return resp.data;
                });
        }
    }
})();
