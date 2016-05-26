(function() {
    'use strict';

    angular.module('app.report')
        .directive('filesUpload', FileUploadDirective);

    function FileUploadDirective(Upload) {
        'ngInject';
        function link(scope, el, attrs, ngModel) {
            console.log('Initial files:', ngModel.$modelValue);
            var div = angular.element(el.find('div')),
                buttonText = div.find('span');

            scope.files = [];

            ngModel.$parsers.push((value) => {
                console.log('value:', value);
            });

            ngModel.$viewChangeListeners.push(() => {
                scope.files = ngModel.$viewValue;
                console.log('Files changes:', ngModel.$viewValue);
//                console.log('Files changes:', scope.$eval('vm.report.files.licenses'));
            });

            scope.$watch('files', () => {
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
                        console.log('Response status:', response.status)
                        // Update button text for single-file uploader
                        if (attrs.multiple === undefined) {
                            buttonText.html(`<small>${file.name}</small>`);
                        }

                        let values = [];
                        if (attrs.multiple !== undefined && ngModel.$viewValue !== undefined) {
                            // Save last model condition
                            values = ngModel.$viewValue;
                        }
                        values.push({
                            id: response.data.id,
                            name: file.name,
                            url: response.data.url
                        });
                        ngModel.$setViewValue(values);
                        ngModel.$setValidity(attrs.ngModel, ngModel.$viewValue.length > 0);

                    }, response => {
                        console.log('Error status: ' + response.status);
                        console.log('Error data: ' + response.data.message);
                        el.append(`
			    <div class="alert alert-danger alert-dismissible" role="alert">
			      <button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>
				${response.data.message}
			    </div>
                        `);
                    });
                });

            });
        }
        return {
            require: 'ngModel',
            restrict: 'E',
            scope: {
                ngModel: '@',
                multiple: '@',
                label: '@'
            },
            template: `
            <div class="fileUpload btn btn-default">
                <span>Выбрать файл</span>
                <input type="file" class="upload" id="{{ngModel}}" name="{{ngModel}}" />
            </div>
            `,
            
            compile: function(tElem, tAttrs) {
                var div = angular.element(tElem.find('div')),
                    buttonText = div.find('span'),
                    fileInput = div.find('input');

                if (tAttrs.label) {
                    let fileLabel = angular.element('<label/>')
                        .addClass('control-label fileUploadLabel')
                        .text(tAttrs.label)
                        .attr('for', tAttrs.ngModel);
                    tElem.prepend(fileLabel);
                }

                if (angular.isDefined(tAttrs.multiple)) {
                    let filesList = angular.element('<files-list />');
                    filesList.attr('files', 'files');

                    tElem.append(filesList);
                    fileInput.attr('multiple', '');
                    buttonText.html('Выбрать файлы');
                }

                return link;
            }
        };
    }
})();
