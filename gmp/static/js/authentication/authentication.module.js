(function() {
    'use strict';

    angular
        .module('gmp.authentication', [
            'gmp.authentication.controllers',
            'gmp.authentication.services'
        ]);

    angular.
        module('gmp.authentication.controllers', []);
    
    angular.
        module('gmp.authentication.services', ['ngCookies']);
})();
