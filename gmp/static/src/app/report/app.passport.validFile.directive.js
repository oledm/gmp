(function() {
    'use strict';

    angular.module('app.passport')
        .directive('validFile', ValidFileDirective);

    function ValidFileDirective() {
        return {
            require: 'ngModel',
            scope: true,
            link: function(scope, el, attrs, ngModel){
                el.bind('change', function(e) {
//                    angular.forEach(e.target.files, function(file) {
//                        Upload.upload({
//                            url: '/api/upload/',
//                            data: {fileupload: file}
//                        }).
//                        then(function(response) {
//                            if (attrs.multiple !== undefined) {
//                                console.log('Multiple Upload');
//                                ngModel.$viewValue[fieldname].push(response.data.id);
//                                el.append('<span>dsds</span>')
//                            } else {
//                                ngModel.$viewValue[fieldname] = [response.data.id];
//                            }
//                        }, function(response) {
//                            console.log('Error status: ' + response.status);
//                        });
//                    });

                    scope.$apply(function(){
                        ngModel.$setViewValue(el.val());
                        ngModel.$render();
                    });
              });
            }
        };
    }
})();
