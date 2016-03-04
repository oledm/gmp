(function() {
    'use strict';

    angular
        .module('app.passport.service')
        .factory('Passport', Passport);

    Passport.$inject = ['$http'];

    function Passport($http) {
        var passport = {
            createPassport: createPassport
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
    }
})();
