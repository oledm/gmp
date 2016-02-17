(function() {
    'use strict';

    angular
        .module('app.userdata.controller')
        .controller('UserDataController', UserDataController);

    UserDataController.$inject = ['Department', 'Authentication', '$log', 'UserData'];

    function UserDataController(Department, Authentication, $log, UserData) {
        var vm = this;

        vm.userdata = UserData;

        $log.log('userdata from UserDataController: ' + JSON.stringify(vm.userdata));
        $log.log('UserDataController cookie: ' + JSON.stringify(cookiedata));

        var cookiedata = Authentication.getAuthenticatedAccount();

        if (cookiedata !== undefined) {
            vm.userdata.email = cookiedata.email || vm.userdata.email;
            vm.userdata.first_name = cookiedata.first_name || vm.userdata.first_name;
            vm.userdata.last_name = cookiedata.last_name || vm.userdata.last_name;
            vm.userdata.department = cookiedata.department || vm.userdata.department;
        }
        console.dir(vm);

        vm.loadDeps = function() {
            Department.query(function(data) {
                vm.allDeps = data;
            });
        };
        
//        vm.updateProfile = function() {
//            var account = Authentication.getAuthenticatedAccount();
//            $log.log('current cookie is ' + JSON.stringify(account));
//            account.department = vm.department;
//            account.first_name = vm.first_name;
//            account.last_name = vm.last_name;
//            account.password = vm.password;
//            account.email = vm.email;
//            $log.log('current cookie is ' + JSON.stringify(account));
//            Authentication.setAuthenticatedAccount(account);
//        };
    }

})();
