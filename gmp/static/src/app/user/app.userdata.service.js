(function() {
    'use strict';

    angular
        .module('app.userdata.service')
        .factory('UserData', UserData);

    UserData.$inject = ['Cookies', '$http', '$q', '$timeout'];

    function UserData(Cookies, $http, $q, $timeout) {
        var data = {
            email: '',
            first_name: '',
            last_name: '',
            department: ''
        };
        var userdata = {
            clean: clean,
            data: data,
            get: get,
            isLoading: false,
            update: update,
            updateSuccessfull: false
        };

        return userdata;

        function clean() {
            angular.forEach(userdata.data, function(v, k) {
                data[k] = '';
            });
        }

        function get() {
            var cookiedata = Cookies.get();
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

            userdata.isLoading = true;
            console.log('Loading indicator start ' + userdata.isLoading);

            angular.forEach(data, function(v, k) {
                cookiedata[k] = data[k];
            });
            Cookies.set(cookiedata);
            return updateDB(cookiedata);
        }

        function updateDB(cookiedata) {
            return $http.put('/api/user/' + cookiedata.username + '/', {
                first_name: data.first_name,
                last_name: data.last_name,
                email: data.email,
                department: data.department
            })
            .then(updateSuccess)
            .catch(updateFailed);

            function updateSuccess(data, status, headers, config) {
                // TODO for demo purpose only updating DB is delayed for 700ms. Remove this later!
                return $timeout(function() {
                    userdata.isLoading = false;
                    userdata.updateSuccessfull = true;

                    // OK-indicator will be shown for 3 seconds
                    $timeout(function() {
                        userdata.updateSuccessfull = false;
                    }, 3000);

                    return data.data;
                }, 700);
            }

            function updateFailed(e) {
                return $q.reject(e);
            }
        }
    }
})();
