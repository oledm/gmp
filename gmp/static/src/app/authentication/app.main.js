(function() {
    'use strict';

    angular
        .module('app.main')
        .controller('MainController', MainController);

    MainController.$inject = ['Authentication', '$location'];

    function MainController(Authentication, $location) {
        var vm = this;
        vm.menu = [
            {name: 'Файлы', link: 'Файлы', icon: 'upload', ref: 'upload'},
            {name: 'Профиль', link: 'Профиль', icon: 'person', ref: 'profile'},
            {name: 'Паспорт двигателя', link: 'Паспорт двигателя', icon: 'document-text', ref: 'passport'},
            {name: 'Заключение', link: 'Заключение', icon: 'document-text', ref: 'report'}
        ];

        activate();

        ///////////////////////////////////////////////

        function activate() {
            if (!Authentication.isAuthenticated()) {
                $location.path('/login');
            }
        }
        vm.isAuthenticated = function() {
            return Authentication.isAuthenticated();
        };
    }
})();

