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
                <h5>Выбранные файлы</h5><li class="list-group-item" 
                ng-repeat="file in files track by $index">{{file.name}}
                <span class="deleteCrossIcon glyphicon glyphicon-remove" aria-hidden="true"
                ng-click="delete(file.id)"></span></li></ul>`,
            link: function(scope, el, attrs) {
                scope.delete = function(id) {
                    scope.files = scope.files.filter(file => file.id !== id);
                    ServerData.delete({category: 'file', categoryId: id});
                };
            }
        };
    }
})();
