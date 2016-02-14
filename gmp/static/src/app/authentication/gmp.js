(function() {
    'use strict';

    angular.module('gmp', [
        'ui.router',
	'ngMaterial',
        'ngMessages',
        'ngResource',
        'ngCookies'
    ])
        .config(['$stateProvider', '$urlRouterProvider', 
                function($stateProvider, $urlRouterProvider) {
            $stateProvider
                .state('home', {
                    url: '/',
                    controller: 'RegisterController',
                    controllerAs: 'vm',
                    templateUrl: '/static/src/app/authentication/register.tpl.html'
                })
                .state('account', {
                    url: '/account',
                    template: 'My personal cabinet'
                })
                .state('tab1', {
                    template: 'TAB1'
                })
                .state('tab2', {
                    template: 'TAB2'
                });
            $urlRouterProvider.otherwise('/');
        }])
        .config(['$mdThemingProvider',
                function($mdThemingProvider) {
            $mdThemingProvider.theme('default')
                .primaryPalette('blue');
        }])
        .config(['$resourceProvider',
                function($resourceProvider) {
            $resourceProvider.defaults.stripTrailingSlashes = false;
        }])
        .config(['$locationProvider',
                function($locationProvider) {
            $locationProvider.html5Mode(true);
            $locationProvider.hashPrefix('!');
        }])
        .run(['$http',
             function($http) {
            $http.defaults.xsrfHeaderName = 'X-CSRFToken';
            $http.defaults.xsrfCookieName = 'csrftoken';
        }])
        .factory('Authentication', ['$http', '$cookies', '$state',
            function($http, $cookies, $state) {
                var Authentication = {
                    register: register,
                    login: login,
                    getAuthenticatedAccount: getAuthenticatedAccount,
                    setAuthenticatedAccount: setAuthenticatedAccount,
                    isAuthenticated: isAuthenticated,
                    unauthenticate: unauthenticate
                };

                return Authentication;

                function register(email, username, password, department) {
                    console.log('register ' + email + ' ' + username + ' ' + password + ' ' + department);
                    return $http.post('/api/user/', {
                        email: email,
                        username: username,
                        password: password,
                        department: department
                    });
                }

                function login(email, password) {
                    return $http.post('/api/login/', {
                        email: 'masdar@list.ru',
                        password: 'ssss'
                    }).then(loginSuccess, loginFail);
                }

                function loginSuccess(response) {
                    Authentication.setAuthenticatedAccount(response.data);
                    $state.go('account');
                }


                function loginFail(response) {
                    console.log('Login failed!!!!!')
                }

                function getAuthenticatedAccount() {
                    if ($cookies.authenticatedAccount) {
                        return;
                    }

                    return JSON.parse($cookies.authenticatedAccount);
                }

                function setAuthenticatedAccount(account) {
                    $cookies.authenticatedAccount = JSON.stringify(account);
                }

                function isAuthenticated() {
                    return !!$cookies.authenticatedAccount;
                }

                function unauthenticate() {
                    delete $cookies.authenticatedAccount;
                }
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

                vm.login = function() {
                    Authentication.login({
                        email: 'masdar@list.ru',
                        password: 'ssss'
                    });
                };

                vm.register = function() {
                    Authentication.register({
                        email: vm.email,
                        username: vm.name,
                        password: 'ssss',
                        department: vm.department
                    });
                };
            }
        ]);
})();
