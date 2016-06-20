(function() {
    'use strict';

    angular
        .module('app.toolbar')
        .controller('ToolbarController', ToolbarController);


    function ToolbarController(Authentication, localStorageService) {
        'ngInject';
        var vm = this;

        vm.logout = function() {
            Authentication.logout()
                .then(() => localStorageService.remove('model'));
        };
    }
})();
