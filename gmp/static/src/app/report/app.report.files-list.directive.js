(function() {
    'use strict';

    angular.module('app.report')
        .directive('filesList', FilesListDirective);

    function FilesListDirective(ServerData) {
        'ngInject';
        return {
            restrict: 'E',
            replace: true,
            scope: {},
            bindToController: {
                files: '&',
                onFilesChange: '&'
            },
            controller: function() {
                var ctrl = this;

                ctrl.extension = name => _(name).split('.').last().toLowerCase();
                ctrl.isPdf = name => ctrl.extension(name) === 'pdf';
                ctrl.isExcel = name => ctrl.extension(name) === 'xls' || ctrl.extension(name) === 'xlsx';

                ctrl.delete = function(id) {
                    let files = ctrl.files().filter(file => file.id !== id);
                    ctrl.onFilesChange({newFilesList: files});
                };
            },
            controllerAs: 'ctrl',
            template: function(tElem, tAttrs) {
                var title = angular.isDefined(tAttrs.multiple) ? 'Выбранные файлы' : 'Выбран файл';

                return `
                <ul class="list-group" ng-class="{hide: ctrl.files().length === 0}">
                <h5>${title}</h5>
                <li class="list-group-item" 
                    ng-repeat="file in ctrl.files() track by $index">{{ !ctrl.isExcel(file.name) ? file.name : '' }}
                    <span class="deleteCrossIcon glyphicon glyphicon-remove" aria-hidden="true"
                    ng-click="ctrl.delete(file.id)"></span>
                    <a ng-href="{{file.url}}"
                        ng-if="!ctrl.isExcel(file.name)"
                        class="thumbnail" target="_blank"
                        ng-switch="ctrl.isPdf(file.name)"
                    >
                        <img ng-switch-when="true" ng-src="{{file.url}}" alt="PDF preview" />
                        <img ng-switch-when="false" ng-src="{{file.url}}" alt="Preview" />
                    </a>
                    <a ng-href="{{file.url}}"
                        ng-if="ctrl.isExcel(file.name)"
                        target="_blank"
                    >
                        {{file.name}}
                    </a>
                </li></ul>`;
            }
        };
    }
})();
