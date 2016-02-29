(function() {
    'use strict';

    angular
        .module('app.config')
        .config(config);

    config.$inject = [
        '$stateProvider',
        '$urlRouterProvider',
        '$resourceProvider',
        '$mdThemingProvider',
        '$locationProvider'
    ];

    function config($stateProvider, $urlRouterProvider, $resourceProvider,
            $mdThemingProvider, $locationProvider) {
        $stateProvider
            .state('home', {
                url: '/'
            })
            .state('profile', {
                url: '/profile',
                controller: 'UserDataController',
                controllerAs: 'vm',
                templateUrl: '/static/src/app/user/profile.tpl.html'
            })
            .state('upload', {
                url: '/upload',
                controller: 'UploadController',
                controllerAs: 'vm',
                templateUrl: '/static/src/app/filestorage/upload.tpl.html'
            })
            .state('passport', {
                url: '/passport',
                controller: 'PassportController',
                controllerAs: 'vm',
                templateUrl: '/static/src/app/report/passport.tpl.html'
            });

        $urlRouterProvider.otherwise('/');

        $resourceProvider.defaults.stripTrailingSlashes = false;

        $mdThemingProvider.theme('default').primaryPalette('blue');

        $locationProvider.html5Mode(true);
        $locationProvider.hashPrefix('!');
    }
})();
