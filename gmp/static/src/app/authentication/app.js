(function() {
    'use strict';

    angular.module('app', [
        'app.config',
        'app.authentication',
        'app.department',
        'app.engine.service',
        'app.main',
        'app.login',
        'app.register',
        'app.cookies',
        'app.userdata.service',
        'app.userdata.controller',
        'app.toolbar',
        'app.upload',
        'app.upload.service',
        'app.passport'
    ]);

    angular
        .module('app')
        .run(['$http',
            function($http) {
                $http.defaults.xsrfHeaderName = 'X-CSRFToken';
                $http.defaults.xsrfCookieName = 'csrftoken';
        }]);

})();
