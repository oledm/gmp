(function() {
    'use strict';

    angular
        .module('app.userdata.controller')
        .controller('UserDataController', UserDataController);

    UserDataController.$inject = ['Department', 'UserData'];

    function UserDataController(Department, UserData) {
        var vm = this;

        vm.loadDepartments = loadDepartments;
        vm.userdata = UserData;

        activate();

        function activate() {
            UserData.get();
        }

	function loadDepartments() {
            Department.query(function(data) {
                vm.allDeps = data;
            });
        }

        vm.updateProfile = function() {
            UserData.update();
        };
    }
})();
