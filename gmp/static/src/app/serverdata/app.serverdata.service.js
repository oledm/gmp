(function() {
    'use strict';

    angular
        .module('app.serverdata')
        .factory('ServerData', ServerData);

    ServerData.$inject = ['$resource'];

    function ServerData($resource) {
        return $resource('/api/:category/');
    }
})();
