(function() {
    'use strict';

    angular.module('app.passport')
        .directive('checkmark', CheckmarkDirective);

    function CheckmarkDirective() {
        return {
            require: '^form',
            restrict: 'A',
            link: function(scope, elem, attrs, formController) {
                scope.$watch(formController.$name + '.$valid', function(newValue, oldValue) {
                    console.log(newValue);
                    if (newValue) {
                        scope.showCheckmark = true;
                    } else {
                        scope.showCheckmark = false;
                    }
                })
            },
            scope: true,
            transclude: true,
            template: '<span ng-if="showCheckmark">' +
                '<i class="icon ion-checkmark" style="color: #00e676"></i>&nbsp;' +
                '</span>' +
                '<span ng-transclude></span>'
        }
    }
})();
