(function() {
    'use strict';

    angular
        .module('app.authentication')
        .factory('Authentication', Authentication);

    Authentication.$inject = ['$http', 'Cookies', '$rootScope', '$state'];

    function Authentication($http, Cookies, $rootScope, $state) {
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

        function register(email, password, department_id) {
            return $http.post('/api/department/' + department_id + '/user/', {
                email: email,
                password: password
            });
        }

        function loginSuccess(response) {
            Cookies.set(response.data);
            $rootScope.$emit('cokkiesSet', '');
            $state.go('home');
        }

        function logoutSuccess() {
            Cookies.remove();
            $rootScope.$emit('cokkiesSet', undefined);
            $state.go('login');
        }

        function loginFail() {
//            $mdDialog
//                .show(
//                    $mdDialog.alert({
//                        title: 'Ошибка',
//                        textContent: 'Неверно указан email/пароль',
//                        ok: 'Закрыть'
//                    }));
        }
    }
})();

