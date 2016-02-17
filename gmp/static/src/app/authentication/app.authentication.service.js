(function() {
    'use strict';

    angular
        .module('app.authentication')
        .factory('Authentication', Authentication_);

    Authentication_.$inject = ['$http', '$cookies', '$mdDialog'];

    function Authentication_($http, $cookies, $mdDialog) {
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
            console.log('cookies: ' + JSON.stringify(Authentication.getAuthenticatedAccount()));
            console.log('Logout failed');
        }
    }
})();

