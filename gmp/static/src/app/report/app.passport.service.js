(function() {
    'use strict';

    angular
        .module('app.passport.service')
        .factory('Passport', Passport);

    Passport.$inject = ['$http'];

    function Passport($http) {
        var passport = {
            createPassport: createPassport,
            getLPUs: getLPUs,
            getOrgs: getOrgs,
        };

        return passport;

        function createPassport(report_data) {
            $http.post('/report/',
                    {'report_data': report_data},
                    { responseType: 'arraybuffer',
                      headers: {'Content-Type': 'application/json'}
                    })
                .success(function(data, status, headers, config) {
                    var file = new Blob([data], {type: 'application/pdf'});
                    saveAs(file, 'report.pdf');
                    return headers;
                });
        }

        function getLPUs(orgId) {
            return $http.get('/api/organization/' + orgId + '/lpu/')
                .then(function(data) {
                    return data.data;
                });
        }

        function getOrgs() {
            return $http.get('/api/organization/')
                .then(function(data) {
                    return data.data;
                });
        }
    }
})();
