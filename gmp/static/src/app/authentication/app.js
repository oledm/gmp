(function() {
    'use strict';

    angular.module('app', [
        'app.config',
        'app.authentication',
        'app.department',
        'app.main',
        'app.login',
        'app.register',
        'app.cookies',
        'app.userdata.service',
        'app.userdata.controller',
        'app.toolbar',
        'app.upload',
    ]);

    angular
        .module('app')
        .run(['$http',
            function($http) {
                $http.defaults.xsrfHeaderName = 'X-CSRFToken';
                $http.defaults.xsrfCookieName = 'csrftoken';
        }]);

})();
