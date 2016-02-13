(function() {
    'use strict';

    angular.module('gmp', [
        'ui.router',
	'ngMaterial',
        'ngMessages',
        'ngResource'
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
        .config(['$mdThemingProvider',
                function($mdThemingProvider) {
            $mdThemingProvider.theme('default')
                .primaryPalette('blue');
        }])
        .config(['$resourceProvider', function($resourceProvider) {
            $resourceProvider.defaults.stripTrailingSlashes = false;
        }])
        .config(['$locationProvider', function($locationProvider) {
            $locationProvider.html5Mode(true);
            $locationProvider.hashPrefix('!');
        }])
        .run(['$http', function($http) {
            $http.defaults.xsrfHeaderName = 'X-CSRFToken';
            $http.defaults.xsrfCookieName = 'csrftoken';
        }])
        .factory('Authentication', ['$resource',
            function($resource) {
                return $resource('/api/user/');
            }
        ])
        .factory('Department', ['$resource',
            function($resource) {
                return $resource('/api/department/');
            }
        ])
        .controller('RegisterController', ['$scope', 'Authentication', 'Department',
            function($scope, Authentication, Department) {
                var vm = this;

                vm.loadDeps = function() {
                    Department.query(function(data) {
                        vm.allDeps = data;
                    });

                };

                vm.send = function() {
                    Authentication.save({
                        email: vm.email,
                        username: vm.name,
                        password: 'ssss',
                        department: vm.department
                    });
                };
            }
        ]);
})();
