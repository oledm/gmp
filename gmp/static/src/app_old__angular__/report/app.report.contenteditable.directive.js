(function() {
    'use strict';

    angular.module('app.report')
        .directive('contenteditable', ContentEditable);

    function ContentEditable() {
        return {
            restrict: "A",
            require: "ngModel",
            link: function(scope, element, attrs, ngModel) {
                function read() {
                    ngModel.$setViewValue(element.html());
                }

                ngModel.$render = function() {
                    element.html(ngModel.$viewValue || "");
                };

                element.bind("blur keypress change", function() {
                    scope.$apply(read);
                    scope.$apply();
                });
            }
        };
    }
})();
