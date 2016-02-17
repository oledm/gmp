(function() {
    'use strict';

    angular
        .module('app.main')
        .controller('MainController', MainController);

    MainController.$inject = ['Authentication'];

    function MainController(Authentication) {
        console.log('MainController');
        var vm = this;

        vm.isAuthenticated = function() {
            return Authentication.isAuthenticated();
        };
    }
})();

