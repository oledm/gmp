(function() {
    'use strict';

    angular.module('gmp', [
            'ui.router',
            'ngMaterial',
            'ngMessages',
            'ngResource',
            'ngCookies'
    ])
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
        .factory('Authentication', ['$http', '$cookies', '$mdDialog',
            function($http, $cookies, $mdDialog) {
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
                    if ($cookies.get('authenticatedAccount') === undefined) {
                        return undefined;
                    }

                    return JSON.parse($cookies.get('authenticatedAccount'));
                }

                function setAuthenticatedAccount(account) {
                    console.log('setAuthenticatedAccount ' + JSON.stringify(account));
                    $cookies.put('authenticatedAccount', JSON.stringify(account));
                    console.log('in cookie: ' + JSON.stringify(Authentication.getAuthenticatedAccount()));
                }

                function isAuthenticated() {
                    return !!$cookies.get('authenticatedAccount');
                }

                function unauthenticate() {
                    $cookies.remove('authenticatedAccount');
                }

                function register(email, username, password, department) {
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
                }

                function loginFail() {
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
                }

                function logoutFailed() {
                    console.log('Logout failed');
                }
            }
        ])
        .factory('Department', ['$resource',
                function($resource) {
                    return $resource('/api/department/');
                }
        ])
        .controller('LoginController', ['Authentication', 
                function(Authentication) {
                    var vm = this;

                    vm.login = login;

                    activate();

                    function login() {
                        console.log('login');
                        Authentication.login(vm.email, vm.password);
                    }

                    function activate() {
                        if (Authentication.isAuthenticated()) {
                        }
                    }

                }
        ])
        .controller('SidenavController', ['Authentication',
            function(Authentication) {
                var vm = this;

                var data = Authentication.getAuthenticatedAccount();
//                console.log('SidenavController cookie: ' + JSON.stringify(data));
                if (data !== undefined) {
                    vm.userdata = {
                        email: data.email,
                        username: data.username,
                        department: data.department
                    };
                }
                console.log('SidenavController vm.userdata is ' + JSON.stringify(vm.userdata));
            }
        ])
        .controller('MainController', ['Authentication',
            function(Authentication) {
                var vm = this;

                vm.isAuthenticated = function() {
                    return Authentication.isAuthenticated();
                };
            }
        ])
        .controller('ToolbarController', ['Authentication',
            function(Authentication) {
                var vm = this;

                vm.logout = function() {
                    Authentication.logout();
                };
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
                    Authentication.login(vm.email, vm.password);
                }

                function registerFail() {
                    console.log('Registration failed');
                }
            }
        ]);
})();
