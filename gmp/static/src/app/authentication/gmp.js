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
                    templateUrl: '/static/src/app/authentication/login_register.tpl.html',
                    controller: function($state) {
                        $state.transitionTo('home.login');
                    }
                })
                .state('home.register', {
                    controller: 'RegisterController',
                    controllerAs: 'vm',
                    templateUrl: '/static/src/app/authentication/register.tpl.html'
                })
                .state('home.login', {
                    controller: 'LoginController',
                    controllerAs: 'vm',
                    templateUrl: '/static/src/app/authentication/login.tpl.html'
                })
                .state('account', {
                    template: 'Личная страница'
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
        .factory('Authentication', ['$http', '$cookies', '$state', '$mdDialog',
            function($http, $cookies, $state, $mdDialog) {
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
                        email: email,
                        password: password
                    }).then(loginSuccess, loginFail);
                }

                function loginSuccess(response) {
                    console.log('loginSuccess');
                    Authentication.setAuthenticatedAccount(response.data);
                    $state.go('account');
                }

                function loginFail(response) {
                    $mdDialog
                        .show(
                            $mdDialog.alert({
                                title: 'Ошибка',
                                textContent: 'Неверно указан email/пароль',
                                ok: 'Закрыть'
                    }));
                }

                function getAuthenticatedAccount() {
                    if ($cookies.get('authenticatedAccount')) {
                        return;
                    }

                    return JSON.parse($cookies.authenticatedAccount);
                }

                function setAuthenticatedAccount(account) {
                    $cookies.put('authenticatedAccount', JSON.stringify(account));
                }

                function isAuthenticated() {
                    return !!$cookies.get('authenticatedAccount');
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
        .controller('LoginController', ['Authentication', '$state', 
            function(Authentication, $state) {
                var vm = this;

                vm.login = login;

                activate();

                function login () {
                    Authentication.login(vm.email, vm.password);
                }

                function activate() {
                    if (Authentication.isAuthenticated()) {
                        console.log('User already authenticated');
                        $state.go('account');
                    }
                }

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

                vm.register = function() {
                    Authentication.register(vm.email, vm.name, vm.password, vm.department)
                        .then(registerSuccess, registerFail);
                };

                function registerSuccess() {
                    console.log('registerSuccess');
                    Authentication.login(vm.email, vm.password);
                }

                function registerFail() {
                    console.log('Registration failed');
                }
            }
        ]);
})();
