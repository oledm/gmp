(function() {
    'use strict';

    angular
        .module('app.serverdata')
        .factory('ServerData', ServerData);

    function ServerData($resource, Cookies) {
        'ngInject';
        return $resource('/api/:category/:categoryId/:subcategory/:subcategoryId', {categoryId: '@id'}, {
            update: {
                method: 'put'
            },
            measurers: {
                method: 'get',
                isArray: true,
                params: {
                    category: 'department',
                    categoryId: () => Cookies.get().department.id,
                    subcategory: 'measurer',
                }
            },
            users: {
                method: 'get',
                isArray: true,
                params: {
                    category: 'department',
                    categoryId: () => Cookies.get().department.id,
                    subcategory: 'user',
                }
            },
            report: {
                url: '/report/',
                method: 'post',
                headers: {'Content-Type': 'application/json'},
                responseType: 'arraybuffer',
                transformResponse: (data, headers, status) => {
                    if (status === 200) {
                        var file = new Blob([data], {type: 'application/pdf'});
                        saveAs(file, 'report.pdf');
                        return headers;
                    }
                }
            }
        });
    }


})();
