(function() {
    'use strict';

    angular
        .module('app.userdata.controller')
        .controller('UserDataController', UserDataController);

    UserDataController.$inject = ['UserData'];

    function UserDataController(UserData) {
        var vm = this;

        vm.updateProfile = updateProfile;
        vm.userdata = UserData;

        activate();

        function activate() {
            UserData.get();
        }

        function updateProfile() {
            UserData.update();
        }
    }
})();
