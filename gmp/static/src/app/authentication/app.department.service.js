(function() {
    'use strict';

    angular
        .module('app.department')
        .factory('Department', Department);

    Department.$inject = ['$resource'];

    function Department($resource) {
        return $resource('/api/department/');
    }
})();
