(function() {
    'use strict';

    angular
        .module('app.config')
        .config(config);

    config.$inject = ['$stateProvider', '$urlRouterProvider'];

    function config($stateProvider, $urlRouterProvider) {
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
    }
})();
