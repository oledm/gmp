(function() {
    'use strict';

    angular.module('app.passport')
        .directive('validFile', ValidFileDirective);

    function ValidFileDirective(Upload) {
        'ngInject';
        return {
            require: 'ngModel',
            scope: {
                ngModel: '='
            },
            link: function(scope, el, attrs, ngModel){
                var fieldname = attrs.name;

                el.bind('change', function(e) {
                    angular.forEach(e.target.files, function(file) {
                        Upload.upload({
                            url: '/api/upload/',
                            data: {fileupload: file}
                        }).
                        then(function(response) {
                            if (attrs.multiple !== undefined) {
                                console.log('Multiple Upload');
                                ngModel.$viewValue[fieldname].push(response.data.id);
                                el.append('<span>dsds</span>')
                            } else {
                                ngModel.$viewValue[fieldname] = [response.data.id];
                            }
                        }, function(response) {
                            console.log('Error status: ' + response.status);
                        });
                    });

//                    scope.$apply(function(){
//                        ngModel.$setViewValue(el.val());
//                        ngModel.$render();
////                        upload(scope.img);
//                    });
              });
            }
        };
    }
})();
