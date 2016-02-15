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
                .state('gmp', {
                    abstract: true,
                    controller: 'ToolbarController',
                    controllerAs: 'vm',
                    templateUrl: '/static/src/app/authentication/toolbar.tpl.html',
                })
                .state('gmp.home', {
                    url: '/',
                    templateUrl: '/static/src/app/authentication/login_register.tpl.html',
                    controller: function($state) {
                        $state.transitionTo('gmp.home.login');
                    }
                })
               .state('gmp.home.register', {
                    controller: 'RegisterController',
                    controllerAs: 'vm',
                    templateUrl: '/static/src/app/authentication/register.tpl.html'
                })
                .state('gmp.home.login', {
                    controller: 'LoginController',
                    controllerAs: 'vm',
                    templateUrl: '/static/src/app/authentication/login.tpl.html'
                })
                .state('gmp.account', {
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
                    logout: logout,
                    getAuthenticatedAccount: getAuthenticatedAccount,
                    setAuthenticatedAccount: setAuthenticatedAccount,
                    isAuthenticated: isAuthenticated,
                    unauthenticate: unauthenticate
                };

                return Authentication;

                function getAuthenticatedAccount() {
                    if ($cookies.get('authenticatedAccount')) {
                        return;
                    }

                    return JSON.parse($cookies.get(authenticatedAccount));
                }

                function setAuthenticatedAccount(account) {
                    $cookies.put('authenticatedAccount', JSON.stringify(account));
                }

                function isAuthenticated() {
                    return !!$cookies.get('authenticatedAccount');
                }

                function unauthenticate() {
                    $cookies.remove('authenticatedAccount');
                }

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
                    $state.go('gmp.account');
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

                function logout() {
                    return $http.post('/api/logout/', {})
                        .then(logoutSuccess, logoutFailed);
                }

                function logoutSuccess() {
                    Authentication.unauthenticate();

                    $state.go('gmp.home')
                }

                function logoutFailed() {
                    console.log('Logut failed');
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
                        console.log('Account is ' + Authentication.getAuthenticatedAccount());
                        $state.go('gmp.account');
                    }
                }

            }
        ])
        .controller('ToolbarController', ['Authentication',
            function(Authentication) {
                var vm = this;

                vm.logout = function() {
                    console.log('logout');
                    Authentication.logout();
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
