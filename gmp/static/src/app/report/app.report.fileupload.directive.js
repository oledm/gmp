(function() {
    'use strict';

    angular.module('app.passport')
        .directive('fileupload', FileUploadDirective);

    function FileUploadDirective(Upload) {
        'ngInject';
        function link(scope, el, attrs, ngModel) {
            el.bind('change', function(e) {
                angular.forEach(e.target.files, function(file) {
                    Upload.upload({
                        url: '/api/upload/',
                        data: {fileupload: file}
                    }).
                    then(function(response) {
                        if (attrs.multiple !== undefined) {
                            console.log('Multiple Upload');
                            ngModel.$viewValue[scope.field].push(response.data.id);
//                            el.append('<span>dsds</span>')
                        } else {
                            ngModel.$viewValue[scope.field] = [response.data.id];
                        }
                    }, function(response) {
                        console.log('Error status: ' + response.status);
                    });
                });
            });

//                    scope.$apply(function(){
//                        ngModel.$setViewValue(el.val());
//                        ngModel.$render();
////                        upload(scope.img);
//                    });
        }
        return {
            require: 'ngModel',
            restrict: 'E',
            scope: {
                ngModel: '=',
                field: '@',
                multiple: '@',
                label: '@'
            },
            template: '<input required {{multiple}} type="file" id="{{field}}" name="{{field}}" />',
            
            compile: function(tElem, tAttrs, transclude) {
                if (tAttrs.label) {
                    var fileLabel = angular.element('<label/>')
                        .addClass('control-label')
                        .text(tAttrs.label)
                        .attr('for', tAttrs.field);
                    tElem.prepend(fileLabel);
                }
                return link;
            }
        };
    }
})();
