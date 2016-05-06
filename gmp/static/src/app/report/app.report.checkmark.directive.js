(function() {
    'use strict';

    angular.module('app.report')
        .directive('checkmark', CheckmarkDirective);

    function CheckmarkDirective() {
        return {
            require: '^form',
            restrict: 'A',
            link: function(scope, elem, attrs, formController) {
                console.log('initial valid is ' + attrs.validon);
//                if (formController.$name === 'vm.docsForm' ||
//                    formController.$name === 'vm.resultsInfoForm' ||
//                    formController.$name === 'vm.resultsTableForm'
//                    ) {
//                    scope.showCheckmark = true;
//                    return;
//                }
                attrs.$observe('validon', function(newValue) {
                    console.log('new valid is ' + newValue);
                    if (!!newValue) {
                        console.log('new valid is TRUTH!!!!!');
                        scope.showCheckmark = true;
                    } else {
                        console.log('new valid is FALSY!!!!!');
                        scope.showCheckmark = false;
                    }
                    console.log('showCheckmark is ' + scope.showCheckmark);
                });
                scope.$watch(formController.$name + '.$valid', function(newValue) {
                    if (newValue) {
                        scope.showCheckmark = true;
                    } else {
                        scope.showCheckmark = false;
                    }
                });
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
