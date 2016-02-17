(function() {
    'use strict';

    angular
        .module('app.profileditor')
        .controller('EditProfileController', EditProfileController);

    EditProfileController.$inject = ['Department', 'Authentication', '$log']

    function EditProfileController(Department, Authentication, $log) {
        var vm = this;

        vm.loadDeps = function() {
            Department.query(function(data) {
                vm.allDeps = data;
            });
        };
        
        vm.updateProfile = function() {
            var account = Authentication.getAuthenticatedAccount();
            $log.log('current cookie is ' + JSON.stringify(account));
            account.department = vm.department;
            account.first_name = vm.first_name;
            account.last_name = vm.last_name;
            account.password = vm.password;
            $log.log('current cookie is ' + JSON.stringify(account));
            Authentication.setAuthenticatedAccount(account);
        };
    }

})();
