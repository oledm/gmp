(function() {
    'use strict';

    angular.module('app.report')
        .directive('filesUpload', FileUploadDirective);

    function FileUploadDirective(Upload) {
        'ngInject';
        function link(scope, el, attrs, ngModel) {
            var div = angular.element(el.find('div'));

            scope.files = [];

            ngModel.$formatters.push((value) => {
                if (angular.isDefined(value)) {
                    scope.files = value;
                }
            });

            ngModel.$viewChangeListeners.push(() => {
                scope.files = ngModel.$viewValue;
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
                        console.log('Successful upload with status', response.status)
                        let values = [];
                        if (attrs.multiple !== undefined && ngModel.$viewValue !== undefined) {
                            // Save last model value
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
                        console.log('Response error status: ' + response.status);
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
            controller: function($scope) {
                var ctrl = this;

                ctrl.updateFiles = updateFiles;

                function updateFiles(newFilesList) {
                    $scope.files = newFilesList;
                }
            },
            controllerAs: 'ctrl',
            template: `
            <div class="fileUpload btn btn-default">
                <span>Выбрать файл</span>
                <input type="file" class="upload" id="{{ngModel}}" name="{{ngModel}}" />
            </div>
            <files-list files="files" on-files-change="ctrl.updateFiles(newFilesList)" />
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

                let filesList = angular.element(tElem.find('files-list'));
                if (angular.isDefined(tAttrs.multiple)) {
                    fileInput.attr('multiple', '');
                    buttonText.html('Выбрать файлы');
                    filesList.attr('multiple', '');
                }

                return link;
            }
        };
    }
})();
