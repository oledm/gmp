(function() {
    'use strict';

    angular
        .module('app.upload')
        .controller('UploadController', UploadController);

    UploadController.$inject = ['$scope', 'UploadService'];

    function UploadController($scope, UploadService) {
        var vm = this;

        vm.files = [];
        vm.upload = upload;

        $scope.fileSelected = fileSelected;

        function fileSelected(element) {
            $scope.$apply(function() {
                vm.files = element.files;
            });
        }

        function upload() {
            angular.forEach(vm.files, function(file) {
                console.log('file: ' + file.name);
                UploadService.upload(file);
                console.dir(file);
            });
        }
    }
})();
