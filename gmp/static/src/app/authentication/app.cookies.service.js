(function() {
    'use strict';

    angular
        .module('app.cookies')
        .factory('Cookies', Cookies);

    Cookies.$inject = ['$cookies', '$log'];

    function Cookies($cookies, $log) {
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
                $log.error('Exception: ' + e);
                return undefined;
            }
        }

        function isSet() {
            return !!$cookies.get(cookieName);
        }

        function set(data) {
            $log.log('cookie set ' + JSON.stringify(data));
            $cookies.put(cookieName, JSON.stringify(data));
            $log.log('in cookie: ' + JSON.stringify(cookies.get()));
        }

        function remove() {
            $cookies.remove(cookieName);
        }
    }
})();
