(function() {
    'use strict';

    angular
        .module('app.upload')
        .controller('UploadController', UploadController);

    UploadController.$inject = ['$scope', 'Upload', 'UploadService'];

    function UploadController($scope, Upload, UploadService) {
        var vm = this;

        $scope.fileSelected = fileSelected;

        vm.files = [];
        vm.upload = upload;
        vm.uploadedFiles = [];
        vm.remove = remove;
        vm.selected = [];
        vm.sortOrder = '-uploaded_at';

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
                Upload.upload({
                    url: '/api/upload/',
                    data: {fileupload: file}
                }).
                then(function(resp) {
                    getUploadedFiles();
                }, function(resp) {
                    console.log('Error status: ' + resp.status);
                });
            });
        }

        function getUploadedFiles() {
            UploadService.query()
                .then(function(resp) {
                    vm.uploadedFiles = resp;
                });
        }

        function remove(item) {
            console.log('До удаления было %s элементов.', vm.uploadedFiles.length);
            angular.forEach(vm.selected, function(file) {
                UploadService.remove(file.id);
                angular.forEach(vm.uploadedFiles, function(v, k) {
                    if (vm.uploadedFiles[k].id === file.id) {
                        vm.uploadedFiles.splice(k, 1);
                    }
                });
            });
            console.log('После удаления осталось %s элементов.', vm.uploadedFiles.length);
        }
    }
})();
