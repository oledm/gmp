(function() {
    'use strict';

    angular
        .module('gmp.routes')
        .controller('config', config);

    config.$inject = ['$stateProvider', '$urlRouterProvider'];

    function config($stateProvider, $urlRouterProvider) {
        $stateProvider
            .state('register', {
                url: '/',
                controller: 'RegisterController',
                controllerAs: 'vm',
                template: 'Provide HTML template here'
            });
        $urlRouterProvider.otherwise('/');
    }
})();
