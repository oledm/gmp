(function() {
    'use strict';

    angular
        .module('app.config')
        .config(config);

    config.$inject = [
        '$stateProvider',
        '$urlRouterProvider',
        '$resourceProvider',
        '$mdThemingProvider',
        '$locationProvider'
    ];

    function config($stateProvider, $urlRouterProvider, $resourceProvider,
            $mdThemingProvider, $locationProvider) {
        $stateProvider
            .state('home', {
                url: '/'
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
            });

        $urlRouterProvider.otherwise('/upload');

        $resourceProvider.defaults.stripTrailingSlashes = false;

//        $mdThemingProvider.theme('default').primaryPalette('blue');

          var blueGreyMap = $mdThemingProvider.extendPalette('blue', {
          });
          // Register the new color palette map with the name <code>neonRed</code>
          $mdThemingProvider.definePalette('blueGrey', blueGreyMap);
          // Use that theme for the primary intentions
//          $mdThemingProvider.theme('default')
//            .primaryPalette('blueGrey');
        $mdThemingProvider.theme('default').primaryPalette('blueGrey', {
	  'hue-3': '500', // use shade 600 for the <code>md-hue-2</code> class
	});

        $locationProvider.html5Mode(true);
        $locationProvider.hashPrefix('!');
    }
})();
