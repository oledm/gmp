(function() {
    'use strict';

    angular
        .module('app.main')
        .controller('MainController', MainController);

    MainController.$inject = ['Authentication'];

    function MainController(Authentication) {
        var vm = this;
        console.log('menu: ' + vm.menu);
        vm.menu = [
            {name: 'Мои файлы', link: 'Файлы', icon: 'upload', ref: 'upload'},
            {name: 'Профиль', link: 'Профиль', icon: 'person', ref: 'profile'},
            {name: 'Паспорт двигателя', link: 'Паспорт двигателя', icon: 'document-text', ref: 'passport'}
        ];

        vm.isAuthenticated = function() {
            return Authentication.isAuthenticated();
        };
    }
})();

