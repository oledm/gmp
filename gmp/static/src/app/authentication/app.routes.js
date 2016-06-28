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
                url: '/',
                controller: 'DashboardController',
                controllerAs: 'vm',
                templateUrl: '/static/src/app/dashboard/main.tpl.html'
            })
            .state('admin', {
                url: '/admin/',
            })
            .state('classic-form', {
                url: '/form',
                templateUrl: '/contact/',
                controller: 'FormController',
                controllerAs: 'vm',
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
                url: '/passport/:id',
                controller: 'PassportController',
                controllerAs: 'vm',
                templateUrl: '/static/src/app/report/passport.tpl.html',
                resolve: {
                    ServerData: 'ServerData',
                    orgs: function(ServerData) {
                        return ServerData.query({category: 'organization'});
                    },
                    allEmployees: function(ServerData) {
                        return ServerData.users().$promise;
                    },
                    allDevices: function(ServerData) {
                        return ServerData.query({category: 'engine'}).$promise;
                    },
                    measurers: function(ServerData) {
                        return ServerData.measurers().$promise;
                    },
                    connection_types: function(ServerData) {
                        return ServerData.query({category: 'connection_types'}).$promise;
                    },
                    allTClasses: function(ServerData) {
                        return ServerData.query({category: 'tclass'}).$promise;
                    }

                },
                data: {
                    type: 'passport'
                }
            })
            .state('report', {
                url: '/report',
                controller: 'ReportController',
                controllerAs: 'vm',
                templateUrl: '/static/src/app/report/report/report.tpl.html'
            })
            .state('report-container', {
                url: '/report-container/:id',
                controller: 'ReportContainerController',
                controllerAs: 'vm',
                templateUrl: '/static/src/app/report/report_container/report.tpl.html',
                resolve: {
                    ServerData: 'ServerData',
                    orgs: function(ServerData) {
                        return ServerData.query({category: 'organization'});
                    },
                    allEmployees: function(ServerData) {
                        return ServerData.users().$promise;
                    },
                    allDevices: function(ServerData) {
                        return ServerData.query({category: 'container'}).$promise;
                    },
                    measurers: function(ServerData) {
                        return ServerData.measurers().$promise;
                    }
                },
                data: {
                    type: 'report-container'
                }
            });

        $urlRouterProvider.otherwise('/');

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
