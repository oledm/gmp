(function() {
    'use strict';

    angular
        .module('app.report')
        .config(ReportConfig);

    function ReportConfig($httpProvider) {
        'ngInject';
        $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
    }
})();
