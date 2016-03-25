(function() {
    'use strict';

    angular.module('app.passport')
        .directive('validFile', ValidFileDirective);

    ValidFileDirective.$inject = ['Upload'];

    function ValidFileDirective(Upload) {
//        function upload(file) {
//            console.log('uploading file ' + file);
//            Upload.upload({
//                url: '/api/upload/',
//                data: {fileupload: file}
//            }).
//            then(function(response) {
//                vm.report.files[fieldname] = response.data.id;
//            }, function(response) {
//                console.log('Error status: ' + response.status);
//            });
//        }

        return {
            require:'ngModel',
            scope: true,
            link:function(scope, el, attrs, ngModel){
                el.bind('change',function(){
                    scope.$apply(function(){
                        ngModel.$setViewValue(el.val());
                        console.log('filename ' + el.val());
                        ngModel.$render();
//                        upload(scope.img);
                    });
              });
            }
        }
    }
})();
