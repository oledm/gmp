(function() {
    'use strict';

    angular
        .module('app.config')
        .config(config)
        .run(run);

    config.$inject = [
        '$stateProvider',
        '$urlRouterProvider',
        '$resourceProvider',
        '$locationProvider'
    ];

    function config($stateProvider, $urlRouterProvider, $resourceProvider, $locationProvider) {
        $stateProvider
            .state('home', {
                url: '/'
            })
            .state('login', {
                url: '/login',
                controller: 'LoginController',
                controllerAs: 'vm',
                templateUrl: '/static/src/app/user/login.tpl.html'
            })
            .state('register', {
                url: '/register',
                controller: 'RegisterController',
                controllerAs: 'vm',
                templateUrl: '/static/src/app/user/register.tpl.html'
            })
            .state('profile', {
                url: '/profile',
                controller: 'UserDataController',
                controllerAs: 'vm',
                templateUrl: '/static/src/app/user/profile.tpl.html'
            })
            .state('upload', {
                url: '/upload',
                controller: 'UploadController',
                controllerAs: 'vm',
                templateUrl: '/static/src/app/filestorage/upload.tpl.html'
            })
            .state('passport', {
                url: '/passport',
                controller: 'PassportController',
                controllerAs: 'vm',
                templateUrl: '/static/src/app/report/passport.tpl.html'
            })
            .state('report', {
                url: '/report',
                controller: 'ReportController',
                controllerAs: 'vm',
                templateUrl: '/static/src/app/report/report/report.tpl.html'
            })
            .state('report-container', {
                url: '/report-container',
                controller: 'ReportContainerController',
                controllerAs: 'vm',
                templateUrl: '/static/src/app/report/report_container/report.tpl.html'
            });

        $urlRouterProvider.otherwise('/login');

        $resourceProvider.defaults.stripTrailingSlashes = false;

        $locationProvider.html5Mode(true);
        $locationProvider.hashPrefix('!');
    }

    function run() {
        var doc = angular.element(document);
        doc.on('click', function() {
            var navbar = doc.find('.navbar-collapse'),
                opened = navbar.hasClass('in');
            if (opened) {
                navbar.collapse('hide');
            }
        });
    }
})();
