(function() {
    'use strict';

    angular
        .module('app.main')
        .controller('MainController', MainController);

    MainController.$inject = ['Authentication', '$location', 'Cookies', '$rootScope'];

    function MainController(Authentication, $location, Cookies, $rootScope) {
        var vm = this;
        vm.menu = [];

        activate();

        ///////////////////////////////////////////////

        function activate() {
            if (!Authentication.isAuthenticated()) {
                $location.path('/login');
            } 

            $rootScope.$on('cokkiesSet', function(event, data) {
                if (data === undefined) {
                    vm.menu = [];
                } else {
                    setupMenu();
                }
            });

            setupMenu();
        }

        function setupMenu() {
                vm.menu = [{name: 'Профиль', link: 'Профиль', ref: 'profile'}];

                var cookies = Cookies.get();
                if (cookies !== undefined) {
                    var report_types = cookies.department.report_types;
                    angular.forEach(report_types, function(report) {
                        vm.menu.push({name: report.name, link: report.name, ref: report.url});
                    });
                }
        }

        vm.isAuthenticated = function() {
            return Authentication.isAuthenticated();
        };
    }
})();
