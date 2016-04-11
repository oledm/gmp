(function() {
    'use strict';

    angular
        .module('app.main')
        .controller('MainController', MainController);

    MainController.$inject = ['Authentication', '$location', 'Department', 'Cookies'];

    function MainController(Authentication, $location, Department, Cookies) {
        var vm = this;
        vm.menu = [
//            {name: 'Файлы', link: 'Файлы', icon: 'upload', ref: 'upload'},
            {name: 'Профиль', link: 'Профиль', icon: 'person', ref: 'profile'},
            {name: 'Паспорт двигателя', link: 'Паспорт двигателя', icon: 'document-text', ref: 'passport'},
            {name: 'Заключение', link: 'Заключение', icon: 'document-text', ref: 'report'},
            {name: 'Отчет по сосудам', link: 'Отчет по сосудам', icon: 'document-text', ref: 'report-container'}
        ];

        activate();

        ///////////////////////////////////////////////

        function activate() {
            if (!Authentication.isAuthenticated()) {
                $location.path('/login');
            } 

            var cookies = Cookies.get();
            if (cookies !== undefined) {
                Department.get({depId: cookies.department.id}, function(data) {
                    console.log('dep data: ' + JSON.stringify(data));
                });
            }
        }
        vm.isAuthenticated = function() {
            return Authentication.isAuthenticated();
        };
    }
})();

