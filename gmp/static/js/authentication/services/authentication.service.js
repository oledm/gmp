(function() {
    'use strict';

    angular
        .module('gmp.authentication.services')
        .factory('Authentication', Authentication);

    Authentication.$inject = ['$cookies', '$http'];

    function Authentication ($cookies, $http) {
        var Authentication = {
            register: register
        };

        return Authentication;

        function register(email, password, username) {
            return $http.post('/api/user/', {
                email: email,
                password: password,
                username: username
            });
        }
    }
})();
