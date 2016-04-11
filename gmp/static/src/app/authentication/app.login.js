(function() {
    'use strict';

    angular
        .module('app.login')
        .controller('LoginController', LoginController);

    LoginController.$inject = ['Authentication', '$state', 'Department', 'Cookies', '$scope'];

    function LoginController(Authentication, $state, Department, Cookies, $scope) {
        var vm = this;

        vm.login = login;

        activate();

        function login() {
            var depId = undefined;
            Authentication.login(vm.email, vm.password)
                .then(function() {
                    depId = Cookies.get().department.id;
                    Department.get({depId: depId}, function(data) {
                        console.log('depId ' + depId);
                        console.log('dep data: ' + JSON.stringify(data));
                    });
                });
//            console.log($scope.$parent.main.menu);
            $state.go('home');
            console.log($scope.$parent.main.menu);
//            console.log('depId ' + depId);
        }

        function activate() {
            if (Authentication.isAuthenticated()) {
                $state.go('home');
            }
        }
    }
})();

