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
                inputFiles: '&files',
                onFilesChange: '&'
            },
            controller: function() {
                var ctrl = this;

                ctrl.isPdf = name => _(name).split('.').last().toLowerCase() === 'pdf';

                ctrl.delete = function(id) {
                    let files = ctrl.inputFiles().filter(file => file.id !== id);
                    ctrl.onFilesChange({newFilesList: files});
                    ServerData.delete({category: 'file', categoryId: id});
                };
            },
            controllerAs: 'ctrl',
            template: function(tElem, tAttrs) {
                var title = angular.isDefined(tAttrs.multiple) ? 'Выбранные файлы' : 'Выбран файл';

                return `
                <ul class="list-group" ng-class="{hide: ctrl.inputFiles().length === 0}">
                <h5>${title}</h5>
                <li class="list-group-item" 
                    ng-repeat="file in ctrl.inputFiles() track by $index">{{file.name}}
                    <span class="deleteCrossIcon glyphicon glyphicon-remove" aria-hidden="true"
                    ng-click="ctrl.delete(file.id)"></span>
                    <a ng-href="{{file.url}}?name={{file.name}}"
                        class="thumbnail" target="_blank"
                        ng-switch="ctrl.isPdf(file.name)"
                    >
                        <img ng-switch-when="true" ng-src="{{file.url}}" alt="PDF preview" />
                        <img ng-switch-when="false" ng-src="{{file.url}}" alt="Preview" />
                    </a>
                </li></ul>`;
            }
        };
    }
})();
