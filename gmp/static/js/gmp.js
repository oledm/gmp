(function() {
    'use strict';

    angular
        .module('gmp', [
            'gmp.authentication',
            'gmp.routes'
        ]);
    
    angular.
        module('gmp.routes', ['ui.router']);
})();
