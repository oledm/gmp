(function() {
    'use strict';

    angular
        .module('app.userdata.service')
        .factory('UserData', UserData);

    UserData.$inject = ['Cookies', '$http'];

    function UserData(Cookies, $http) {
        var data = {
            email: '',
            first_name: '',
            last_name: '',
            department: ''
        };
        var userdata = {
            data: data,
            clean: clean,
            update: update,
            get: get
        };

        return userdata;

        function clean() {
            angular.forEach(userdata.data, function(v, k) {
//                console.log('clean value ' + v + ' of key ' + k);
                data[k] = '';
            });
        }

        function get() {
            var cookiedata = Cookies.get();
            console.log('cookie data: ' + JSON.stringify(cookiedata));
            console.log('user data: ' + JSON.stringify(userdata.data));
            if (cookiedata !== undefined) {
                data.email = cookiedata.email;
                data.first_name = cookiedata.first_name;
                data.last_name = cookiedata.last_name;
                data.department = cookiedata.department;
                userdata.data = data;
            }
            console.log('updated user data: ' + JSON.stringify(userdata.data));
        }

        function update() {
            var cookiedata = Cookies.get();

            angular.forEach(data, function(v, k) {
                console.log('updating cookie key ' + k + ' with value ' + data[k]);
                cookiedata[k] = data[k];
            });
            Cookies.set(cookiedata);
//            console.log('updated cookie: ' + JSON.stringify(Cookies.get()));
            update_db(cookiedata);
        }

        function update_db(cookiedata) {
            $http.put('/api/user/' + cookiedata.username + '/', {
                first_name: data.first_name,
                last_name: data.last_name,
                email: data.email,
                department: data.department
            });
        }
    }
})();
