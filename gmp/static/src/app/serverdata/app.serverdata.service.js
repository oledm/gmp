(function() {
    'use strict';

    angular
        .module('app.serverdata')
        .factory('ServerData', ServerData);

    function ServerData($resource, Cookies) {
        'ngInject';
        return $resource('/api/:category/:categoryId/:subcategory/:subcategoryId', {categoryId: '@id'}, {
            measurers: {
                method: 'get',
                isArray: true,
                params: {
                    category: 'department',
                    categoryId: Cookies.get().department.id,
                    subcategory: 'measurer',
                }
            },
            users: {
                method: 'get',
                isArray: true,
                params: {
                    category: 'department',
                    categoryId: Cookies.get().department.id,
                    subcategory: 'user',
                }
            }
        });
    }
})();
