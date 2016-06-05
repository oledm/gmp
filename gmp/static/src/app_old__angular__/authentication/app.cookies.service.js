(function() {
    'use strict';

    angular
        .module('app.cookies')
        .factory('Cookies', Cookies);

    function Cookies($cookies) {
        'ngInject';
        var cookieName = 'authentcatedAccount';
        var cookies = {
            get: get,
            isSet: isSet,
            set: set,
            remove: remove
        };

        return cookies;

        function get() {
            try {
                return JSON.parse($cookies.get(cookieName));
            }
            catch(e) {
                return undefined;
            }
        }

        function isSet() {
            return !!$cookies.get(cookieName);
        }

        function set(data) {
//            $log.log('cookie to be set ' + JSON.stringify(data));
            $cookies.put(cookieName, JSON.stringify(data));
//            $log.log('in cookie: ' + JSON.stringify(cookies.get()));
        }

        function remove() {
//            console.log('before delete ' + JSON.parse($cookies.get(cookieName)));
            $cookies.remove(cookieName);
//            console.log('after delete ' + $cookies.get(cookieName));
        }
    }
})();
