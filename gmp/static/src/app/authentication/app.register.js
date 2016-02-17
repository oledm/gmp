(function() {
    angular
        .module('app.register')
        .controller('RegisterController', RegisterController);

    RegisterController.$inject = ['Authentication', 'Department'];

    function RegisterController(Authentication, Department) {
        var vm = this;

        vm.loadDeps = function() {
            Department.query(function(data) {
                vm.allDeps = data;
            });
        };

        vm.register = function() {
            Authentication.register(vm.email, vm.name, vm.password, vm.department)
                .then(registerSuccess, registerFail);
        };

        function registerSuccess() {
            Authentication.login(vm.email, vm.password);
        }

        function registerFail() {
            console.log('Registration failed');
        }
    }
})();

