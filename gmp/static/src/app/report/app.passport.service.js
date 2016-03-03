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
        function createPassport() {
            return $http.get('/passport/')
                .then(function(response) {
                    return response;
                });
        }
    }
})();
