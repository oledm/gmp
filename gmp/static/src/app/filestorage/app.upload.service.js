(function() {
    'use strict';

    angular
        .module('app.upload.service')
        .factory('UploadService', UploadService);

    UploadService.$inject = ['$http'];
    function UploadService($http, Upload) {
        var service = {
            upload: upload
        };

        return service;

        function upload(file) {
            console.log('Отправка файла ' + file);
            return $http.post('/api/storage/', {fileupload: file});
        }
    }
})();
