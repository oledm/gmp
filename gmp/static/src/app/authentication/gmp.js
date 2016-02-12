'use strict';

(function() {
    angular.module('gmp', [
        'ui.router',
    ])
        .config(['$stateProvider', '$urlRouterProvider', 
                function($stateProvider, $urlRouterProvider) {
            $stateProvider.state(
                'home', {
                    url: '/',
                    controller: 'RegisterController',
                    controllerAs: 'vm',
                    templateUrl: '/static/src/app/authentication/register.tpl.html'
                }
            );
            $urlRouterProvider.otherwise('/');
        }])
        .factory('Authentication', ['$http', 
            function($http) {
                return {register: register};

                function register(email, username, password, department) {
                    return $http.post('/api/user/', {
                        email: email,
                        username: username,
                        password: password,
                        department: department
                    });
                }
            }
        ])
        .controller('RegisterController', ['$scope', 'Authentication',
            function($scope, Authentication) {
                var vm = this;
                vm.test = 'Angular data';
                Authentication.register('masdar@list.ru', 'AngularUser', 'ssss', 'Первый отдел');
            }
        ]);
})();
