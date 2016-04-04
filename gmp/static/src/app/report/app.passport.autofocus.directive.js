(function() {
    'use strict';

    angular.module('app.passport')
        .directive('autofocus', AutofocusDirective);

    AutofocusDirective.$inject = ['$timeout']
    function AutofocusDirective($timeout) {
	return {
	    restrict: 'A',
	    link : function($scope, $element) {
		    $timeout(function() {
		    $element.focus();
		});
	    }
	}
    }
})();

