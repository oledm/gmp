(function() {
    'use strict';

    angular
        .module('app.userdata.controller')
        .controller('UserDataController', UserDataController);

    UserDataController.$inject = ['Department', 'UserData'];

    function UserDataController(Department, UserData) {
        var vm = this;

        vm.loadDepartments = loadDepartments;
        vm.updateProfile = updateProfile;
        vm.userdata = UserData;

        activate();

        function activate() {
            UserData.get();
            loadDepartments();
        }

	function loadDepartments() {
            Department.query(function(data) {
                vm.allDeps = data;
            });
        }

        function updateProfile() {
            UserData.update();
        }
    }
})();
