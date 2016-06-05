(function() {
    'use strict';

    angular.module('app.login')
        .directive('gmpInput', gmpInput);

    function gmpInput () {
        return {
            restrict: 'E',
//            controller: function($scope, $element) {
//                console.log($element.attr('name'));
//                $scope.hasError = this.field.$touched && this.field.$invalid;
//
//            },
            link: function(scope) {
                scope.isValid = scope.userForm.email.$touched;
//                scope.userForm.email.$touched.$watch()

            },
//            compile: function(tElem, tAttrs) {
//                console.log('attrs: ' + tAttrs.id);
//                tElem.find('label').attr('for', tAttrs.id);
//                tElem.find('input').attr('id', tAttrs.id);
//                tElem.find('input').attr('name', 'email');
//            },
//            scope: {
//                type: '@',
//                model: '=ngModel',
//                field: '=',
//                placeholder: '@'
//            },
            templateUrl: '/static/src/app/user/gmp-input.directive.tpl.html'
        };
    }
})();
