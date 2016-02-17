(function() {
    'use strict';

    angular
        .module('app.toolbar')
        .controller('ToolbarController', ToolbarController);

    ToolbarController.$inject = ['Authentication', '$state'];

    function ToolbarController(Authentication, $state) {
        var vm = this;

        vm.logout = function() {
            Authentication.logout();
            $state.go('home');
        };
    }
})();
