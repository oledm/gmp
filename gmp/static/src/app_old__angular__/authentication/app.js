(function() {
    'use strict';

    angular
        .module('app')
        .run(function($http, amMoment) {
            'ngInject';
            $http.defaults.xsrfHeaderName = 'X-CSRFToken';
            $http.defaults.xsrfCookieName = 'csrftoken';
            amMoment.changeLocale('ru');
        });
})();
