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

        function getLPUs() {
            console.log('getLPUs');
            return $http.get('/api/organization/1/lpu/')
                .then(function(data) {
                    console.log('LPU list: ' + data.data);
                    return data.data;
                });
        }
    }
})();
