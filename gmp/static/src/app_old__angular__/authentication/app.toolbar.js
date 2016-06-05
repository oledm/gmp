(function() {
    'use strict';

    angular
        .module('app.toolbar')
        .controller('ToolbarController', ToolbarController);

    ToolbarController.$inject = ['Authentication'];

    function ToolbarController(Authentication) {
        var vm = this;

        vm.logout = function() {
            Authentication.logout();
        };
    }
})();
