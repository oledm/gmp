(function() {
    'use strict';

    angular
        .module('app.login')
        .controller('LoginController', LoginController);

    LoginController.$inject = ['Authentication', '$state', '$rootScope'];

    function LoginController(Authentication, $state, $rootScope) {
        var vm = this;

        vm.login = login;

        activate();

        function login() {
            Authentication.login(vm.email, vm.password)
                .then(loginSuccess);
        }

        function loginSuccess() {
            $rootScope.$emit('cokkiesSet', '');
            $state.go('home');
        }

        function activate() {
            if (Authentication.isAuthenticated()) {
                $state.go('home');
            }
        }
    }
})();

