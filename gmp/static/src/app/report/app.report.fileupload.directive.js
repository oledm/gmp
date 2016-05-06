(function() {
    'use strict';

    angular.module('app.passport')
        .directive('filesList', FilesListDirective)
        .directive('filesUpload', FileUploadDirective);

    function FilesListDirective() {
        'ngInject';
        return {
            restrict: 'E',
            replace: true,
            scope: {
                files: '='
            },
            template: '<ul class="list-group" ng-class="{hide: files.length === 0}">' + 
                '<h5>Выбранные файлы</h5>' + 
                '<li class="list-group-item" ' + 
                'ng-repeat="file in files track by $index">{{file.name}}' + 
                '<span class="deleteCrossIcon glyphicon glyphicon-remove" aria-hidden="true"' + 
                'ng-click="delete(file.id)"></span>' +
                '</li>' +
                '</ul>',
            link: function(scope, el, attrs) {
                scope.delete = function(id) {
                    console.log('delete ' + id);
                    scope.files = scope.files.filter(file => file.id !== id);
                    console.log('new files is ' + JSON.stringify(scope.files));
                };
            }
        };
    }

    function FileUploadDirective(Upload) {
        'ngInject';
        function link(scope, el, attrs, ngModel) {
            scope.files = [];

//            ngModel.$formatters.push(modelValue => {
//                console.log('formatters');
//                return modelValue;
//            });
            
//            ngModel.$parsers.push(viewValue => {
//                console.log(`parsers: ${JSON.stringify(viewValue)}`);
//                return viewValue;
//            });
//            
//            ngModel.$render(() => {
//                scope.files = ngModel.$viewValue;
//                console.log(`model from render: ${scope.files}`);
//            });

//            ngModel.$viewChangeListeners.push(() => {
//                console.log('viewChangeListeners');
//                scope.files = ngModel.$viewValue;
//            });

            scope.$watch('files', () => {
//                console.log(`files changes somewhere: ${JSON.stringify(scope.files)}`);
                ngModel.$setViewValue(scope.files);
                ngModel.$setValidity(attrs.ngModel, ngModel.$viewValue.length > 0);
            });

            el.bind('change', event => {
                angular.forEach(event.target.files, file => {
                    Upload.upload({
                        url: '/api/upload/',
                        data: {fileupload: file}
                    }).
                    then(response => {
                        let values = [];

                        if (attrs.multiple !== undefined && ngModel.$viewValue !== undefined) {
                            // Save last model condition
                            values = ngModel.$viewValue;
                        }
                        values.push({id: response.data.id, name: file.name});
                        ngModel.$setViewValue(values);
                        ngModel.$setValidity(attrs.ngModel, ngModel.$viewValue.length > 0);
                    }, response => {
                        console.log('Error status: ' + response.status);
                    });
                });

            });
        }
        return {
            require: 'ngModel',
            restrict: 'E',
            scope: {
                multiple: '@',
                label: '@'
            },
            template: `
            <input required type="file" id="dsdsdsdlksjh" name="dsdsdsdlksjh" />
            <files-list files="files"><files-list/>
            `,
            
            compile: function(tElem, tAttrs) {
                var fileInput = angular.element(tElem.children()[0]);

                if (tAttrs.multiple !== undefined) {
                    fileInput.attr('multiple', '');
                }

                if (tAttrs.label) {
                    var fileLabel = angular.element('<label/>')
                        .addClass('control-label')
                        .text(tAttrs.label)
                        .attr('for', tAttrs.ngModel);
                    tElem.prepend(fileLabel);
                }
                return link;
            }
        };
    }
})();
