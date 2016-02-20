(function() {
    'use strict';

    angular
        .module('app.upload')
        .controller('UploadController', UploadController);

    UploadController.$inject = ['$scope', 'Upload'];

    function UploadController($scope, Upload) {
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
                Upload.upload({
                    url: '/api/storage/',
                    data: {fileupload: file},
                });
	    });
        }
    }
})();
