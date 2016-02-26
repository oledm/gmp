(function() {
    'use strict';

    angular
        .module('app.authentication')
        .factory('Authentication', Authentication);

    Authentication.$inject = ['$http', '$mdDialog', 'Cookies'];

    function Authentication($http, $mdDialog, Cookies) {
        var authentication = {
            isAuthenticated: isAuthenticated,
            login: login,
            logout: logout,
            register: register
        };

        return authentication;

        function isAuthenticated() {
            return Cookies.isSet();
        }

        function login(email, password) {
            return $http.post('/api/login/', {
                email: email,
                password: password
            }).then(loginSuccess, loginFail);
        }

        function logout() {
            return $http.post('/api/logout/', {})
                .then(logoutSuccess);
        }

        function register(email, username, password, department) {
            return $http.post('/api/user/', {
                email: email,
                username: username,
                password: password,
                department: {
                    name: department
                }
            });
        }

        function loginSuccess(response) {
//            console.log('Cookies before: ' + Cookies.get());
            Cookies.set(response.data);
//            console.log('Cookies after: ' + JSON.stringify(Cookies.get()));
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

        function logoutSuccess() {
            Cookies.remove();
        }
    }
})();

