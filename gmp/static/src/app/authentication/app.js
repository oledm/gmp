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
        .config(['$resourceProvider',
            function($resourceProvider) {
                $resourceProvider.defaults.stripTrailingSlashes = false;
        }])
        .config(['$locationProvider',
            function($locationProvider) {
                $locationProvider.html5Mode(true);
                $locationProvider.hashPrefix('!');
        }])
        .config(['$mdThemingProvider',
            function($mdThemingProvider) {
                $mdThemingProvider.theme('default')
                    .primaryPalette('blue');
        }])
        .run(['$http',
            function($http) {
                $http.defaults.xsrfHeaderName = 'X-CSRFToken';
                $http.defaults.xsrfCookieName = 'csrftoken';
        }]);

//            'ngMaterial',
//            'ngMessages',
//            'ngResource',
})();
