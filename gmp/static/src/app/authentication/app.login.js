(function() {
    'use strict';

    angular
        .module('app.login')
        .controller('LoginController', LoginController);

    function LoginController(Authentication) {
        'ngInject';
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

