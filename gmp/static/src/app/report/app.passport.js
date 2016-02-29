(function() {
    'use strict';

    angular
        .module('app.passport')
        .controller('PassportController', PassportController);

//    PassportController.$inject = [];
    function PassportController() {
        var vm = this;

        vm.test = 'PassportController';
    }
})();
