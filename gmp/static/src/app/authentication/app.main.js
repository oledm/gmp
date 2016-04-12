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

            $rootScope.$on('cokkiesSet', function(event, args) {
                setupMenu();
            });

            setupMenu();
        }

        function setupMenu() {
            if (vm.menu.length === 0) {
                var cookies = Cookies.get();
                if (cookies !== undefined) {
                    var report_types = cookies.department.report_types;
                    vm.menu.push({name: 'Профиль', link: 'Профиль', ref: 'profile'});
                    angular.forEach(report_types, function(el) {
                        vm.menu.push(
                            {name: el.name, link: el.name, ref: el.url}
                        );
                    });
                }
            }
        }
        vm.isAuthenticated = function() {
            return Authentication.isAuthenticated();
        };
    }
})();

