(function() {
    'use strict';

    angular
        .module('app.userdata.controller')
        .controller('UserDataController', UserDataController);

    UserDataController.$inject = ['Department', 'UserData'];

    function UserDataController(Department, UserData) {
        var vm = this;

        vm.userdata = UserData.data;
        vm.loadDeps = loadDeps;

	function loadDeps() {
            Department.query(function(data) {
                vm.allDeps = data;
            });
        }

        vm.updateProfile = function() {
            UserData.update();
        };
    }
})();
