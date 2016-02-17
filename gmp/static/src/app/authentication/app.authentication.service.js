(function() {
    'use strict';

    angular
        .module('app.authentication')
        .factory('Authentication', Authentication);

    Authentication.$inject = ['$http', '$cookies', '$mdDialog'];

    function Authentication($http, $cookies, $mdDialog) {
        return {
            register: register,
            login: login,
            logout: logout,
            getAuthenticatedAccount: getAuthenticatedAccount,
            setAuthenticatedAccount: setAuthenticatedAccount,
            isAuthenticated: isAuthenticated,
            unauthenticate: unauthenticate
        };

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
})();

