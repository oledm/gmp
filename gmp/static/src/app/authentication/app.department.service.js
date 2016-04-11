(function() {
    'use strict';

    angular
        .module('app.department')
        .factory('Department', Department);

    Department.$inject = ['$resource'];

    function Department($resource) {
        return $resource('/api/department/:depId/', {}, {
            measurers: {
                method: 'get',
                isArray: true,
                params: {depId: 1},
                url: '/api/department/:depId/measurer/'
            }
        });
    }
})();
