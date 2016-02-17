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

    function config($stateProvider, $urlRouterProvider, $resourceProvider, $mdThemingProvider, $locationProvider) {
        $stateProvider
            .state('home', {
                url: '/'
            })
            .state('profile', {
                url: '/profile',
                controller: 'EditProfileController',
                controllerAs: 'vm',
                templateUrl: '/static/src/app/authentication/profile.tpl.html'
            });

        $urlRouterProvider.otherwise('/');

        $resourceProvider.defaults.stripTrailingSlashes = false;

        $mdThemingProvider.theme('default').primaryPalette('blue');

        $locationProvider.html5Mode(true);
        $locationProvider.hashPrefix('!');
    }
})();
