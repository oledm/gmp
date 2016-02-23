(function() {
    'use strict';

    angular
        .module('app.main')
        .controller('MainController', MainController);

    MainController.$inject = ['Authentication'];

    function MainController(Authentication) {
        var vm = this;
        vm.menu = {name: "Загрузка файлов"};

        vm.isAuthenticated = function() {
            return Authentication.isAuthenticated();
        };
    }
})();

