(function() {
    'use strict';

    angular.module('app.report')
        .directive('filesList', FilesListDirective);

    function FilesListDirective(ServerData) {
        'ngInject';
        return {
            restrict: 'E',
            replace: true,
            scope: {
                files: '='
            },
            template: `<ul class="list-group" ng-class="{hide: files.length === 0}">
                <h5></h5>
                <li class="list-group-item" 
                    ng-repeat="file in files track by $index">{{file.name}}
                    <span class="deleteCrossIcon glyphicon glyphicon-remove" aria-hidden="true"
                    ng-click="delete(file.id)"></span>
                    <a ng-href="{{file.url}}?name={{file.name}}"
                        class="thumbnail" target="_blank"
                        ng-switch="isPdf(file.name)"
                    >
                        <img ng-switch-when="true" ng-src="{{file.url}}" alt="PDF preview" />
                        <img ng-switch-when="false" ng-src="{{file.url}}" alt="Preview" />
                    </a>
                </li></ul>`,
            compile: function(tElem, tAttrs) {
                var header = angular.element(tElem.find('h5')),
                    title = angular.isDefined(tAttrs.multiple) ? 'Выбранные файлы' : 'Выбран файл';
                header.html(title);

                return function(scope, el, attrs) {
                    scope._ = _;

                    scope.isPdf = name => _(name).split('.').last().toLowerCase() === 'pdf';

                    scope.delete = function(id) {
                        scope.files = scope.files.filter(file => file.id !== id);
                        ServerData.delete({category: 'file', categoryId: id});
                    };
                }
            }
        };
    }
})();
