(function() {
    'use strict';

    angular
        .module('app.login')
        .controller('LoginController', LoginController);

    LoginController.$inject = ['Authentication', '$state'];

    function LoginController(Authentication, $state) {
        var vm = this;

        vm.login = login;

        activate();

        function login() {
            Authentication.login(vm.email, vm.password);
            $state.go('home');
        }

        function activate() {
            if (Authentication.isAuthenticated()) {
                $state.go('home');
            }
        }
    }
})();

