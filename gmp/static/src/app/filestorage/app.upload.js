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

        $scope.fileSelected = fileSelected;


        function fileSelected(element) {
            $scope.$apply(function() {
                vm.files = element.files;
            });
        }

        function upload() {
            angular.forEach(vm.files, function(file) {
                console.log('file: ' + file.name);
                Upload.upload({
                    url: '/api/upload/',
                    data: {fileupload: file}
                }).
                then(function(resp) {
                    console.log('Success ' + resp.config.data.fileupload.name + ' uploaded');
                    UploadService.getFiles()
                        .then(function(resp) {
                            vm.uploadedFiles = resp;
                            console.log(resp);
                        });
                }, function(resp) {
                    console.log('Error status: ' + resp.status);
                });
            });
        }
    }
})();
