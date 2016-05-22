(function() {
    'use strict';

    angular.module('app.report')
        .directive('checkmark', CheckmarkDirective);

    function CheckmarkDirective() {

        return {
            require: '^form',
            restrict: 'A',
            link: function(scope, elem, attrs, formController) {
                if (attrs.validOn !== undefined) {
                    attrs.$observe('validOn', function(newValue) {
                        newValue = scope.$eval(newValue)
                        setCheckMark(newValue);
                    });
                } else {
                    scope.$watch(formController.$name + '.$valid', function(newValue) {
                        setCheckMark(newValue);
                    });
                }
                ///////////////////////////////////////////////////
                function setCheckMark(value) {
                    if (value) {
                        scope.showCheckmark = true;
                    } else {
                        scope.showCheckmark = false;
                    }
                }

            },
            scope: true,
            transclude: true,
            template: '<span ng-if="showCheckmark">' +
                '<i class="glyphicon glyphicon-ok" style="color: #00e676"></i>&nbsp;' +
                '</span>' +
                '<span ng-transclude></span>'
        };
    }
})();
