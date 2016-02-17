(function() {
    'use strict';

    angular.module('app', [
        'app.config',
        'app.authentication',
        'app.department',
        'app.main',
        'app.login',
        'app.register',
        'app.toolbar',
        'app.sidenav',
        'app.profileditor'
    ]);

    angular
        .module('app')
        .run(['$http',
            function($http) {
                $http.defaults.xsrfHeaderName = 'X-CSRFToken';
                $http.defaults.xsrfCookieName = 'csrftoken';
        }]);

})();
