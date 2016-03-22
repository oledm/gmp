(function() {
    'use strict';

    angular.module('app.login')
        .directive('gmpInput', gmpInput);

    function gmpInput () {
        return {
            restrict: 'AE',
            replace: true,
            scope: {
                field: '=',
                model: '='
            },
            templateUrl: "/static/src/app/user/gmp-input.directive.tpl.html"
        };
    }
})();
