(function() {
    'use strict';

    angular
        .module('app.login')
        .controller('LoginController', LoginController);

    LoginController.$inject = ['Authentication'];

    function LoginController(Authentication) {
        var vm = this;

        vm.login = login;

        activate();

        function login() {
            Authentication.login(vm.email, vm.password);
        }

        function activate() {
            if (Authentication.isAuthenticated()) {
                $state.go('home');
            }
        }
    }
})();

