(function() {
    'use strict';

    angular
        .module('app')
        .run(['$http',
            function($http) {
                $http.defaults.xsrfHeaderName = 'X-CSRFToken';
                $http.defaults.xsrfCookieName = 'csrftoken';
        }]);

})();
