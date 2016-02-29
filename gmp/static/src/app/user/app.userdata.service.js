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
            getAllUsers: getAllUsers,
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
            var cookie = Cookies.get();
            console.log('cookies: ' + JSON.stringify(cookie));
            angular.forEach(cookie, function(v, k) {
                if (k in data) {
                    data[k] = cookie[k];
                }
            });
            console.log('updated user data: ' + JSON.stringify(userdata.data));
        }

        function getAllUsers() {
            return $http.get('/api/user/').then(
                getAllUsersSuccess
            );
        }

        function getAllUsersSuccess(response) {
            return response.data.map(function(user) {
                return user.last_name + ' ' + user.first_name;
            });
        }

        function update() {
            var cookie = Cookies.get();

            userdata.isLoading = true;
            userdata.updateSuccessfull = false;

            angular.forEach(data, function(v, k) {
                cookie[k] = data[k];
                console.log('updating with value ' + data[k]);
            });

            Cookies.set(cookie);
            return updateDB(cookie);
        }

        function updateDB(cookie) {
            return $http.put('/api/user/' + cookie.username + '/', {
                first_name: data.first_name,
                last_name: data.last_name,
                email: data.email,
                department: data.department
            })
            .then(updateSuccess)
            .catch(updateFailed);
        }

        function updateSuccess(response) {
            // TODO Only for demo purpose updating DB is delayed for 700ms.
            // Remove this later!
            return $timeout(function() {
                userdata.isLoading = false;
                userdata.updateSuccessfull = true;

                // OK-indicator will be shown for 3 seconds
                $timeout(function() {
                    userdata.updateSuccessfull = false;
                }, 3000);

                console.log('Data from update: %s', JSON.stringify(response.data));
                console.log('Status from update: %s', response.status);
                return response.data;
            }, 700);
        }

        function updateFailed(e) {
            return $q.reject(e);
        }
    }
})();
