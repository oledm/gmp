(function() {
    'use strict';

    angular
        .module('app.upload')
        .controller('UploadController', UploadController);

    UploadController.$inject = ['$scope', 'Upload', 'UploadService'];

    function UploadController($scope, Upload, UploadService) {
        var vm = this;

        vm.files = [];
        vm.upload = upload;
        vm.uploadedFiles = [];
        vm.selected = [];
        vm.sortOrder = '-uploaded_at';

        $scope.fileSelected = fileSelected;

        activate();

        function activate() {
            getUploadedFiles();
        }

        function fileSelected(element) {
            upload(element.files);
            getUploadedFiles();
        }

        function upload(files) {
            angular.forEach(files, function(file) {
                console.log('file: ' + file.name);
                Upload.upload({
                    url: '/api/upload/',
                    data: {fileupload: file}
                }).
                then(function(resp) {
//                    console.log('Success ' + resp.config.data.fileupload.name + ' uploaded');
                    getUploadedFiles();
                }, function(resp) {
                    console.log('Error status: ' + resp.status);
                });
            });
        }

        function getUploadedFiles() {
            UploadService.getFiles()
                .then(function(resp) {
                    vm.uploadedFiles = resp;
                });
        }
    }
})();
