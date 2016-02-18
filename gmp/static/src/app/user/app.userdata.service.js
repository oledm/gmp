(function() {
    'use strict';

    angular
        .module('app.userdata.service')
        .factory('UserData', UserData);

    UserData.$inject = ['Cookies'];

    function UserData(Cookies) {
        var data = {
            email: '',
            first_name: '',
            last_name: '',
            department: ''
        };
        var userdata = {
            data: data,
            clean: clean,
            update: update
        };

	activate();

        return userdata;

        function activate() {
//            console.log('userdata from UserDataService: ' + JSON.stringify(userdata));
            var cookiedata = Cookies.get();
            console.log('cookie data: ' + JSON.stringify(cookiedata));
            if (cookiedata !== undefined) {
                data.email = cookiedata.email || data.email;
                data.first_name = cookiedata.first_name || data.first_name;
                data.last_name = cookiedata.last_name || data.last_name;
                data.department = cookiedata.department || data.department;
            }
//            console.log('userdata after cookie ' + JSON.stringify(userdata));
        }

        function clean() {
            angular.forEach(userdata.data, function(v, k) {
//                console.log('clean value ' + v + ' of key ' + k);
                data[k] = '';
            });
        }

        function update() {
            var cookiedata = Cookies.get();

            angular.forEach(data, function(v, k) {
                console.log('updating cookie key ' + k + ' with value ' + data[k]);
                cookiedata[k] = data[k];
            });
            Cookies.set(cookiedata);
            console.log('updated cookie: ' + JSON.stringify(Cookies.get()));
        }
    }
})();
