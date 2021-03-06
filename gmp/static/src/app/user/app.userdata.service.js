(function() {
    'use strict';

    angular
        .module('app.userdata.service')
        .factory('UserData', UserData);

    function UserData(Cookies, $http, $q) {
        'ngInject';

        var data = {
            email: '',
            first_name: '',
            last_name: '',
            middle_name: '',
            department: '',
            password: '',
            confirm_password: ''
        };
        var userdata = {
            clean: clean,
            data: data,
            get: get,
            getAllUsers: getAllUsers,
            isLoading: false,
            update: update,
//            updateSuccessfull: false
        };

        return userdata;

        function clean() {
            angular.forEach(userdata.data, function(v, k) {
                data[k] = '';
            });
        }

        function get() {
            var cookie = Cookies.get();
            angular.forEach(cookie, function(v, k) {
                if (k in data) {
                    data[k] = cookie[k];
                }
            });
        }

        function getAllUsers() {
            var cookie = Cookies.get();
            return $http.get('/api/department/' + cookie.department.id + '/user/').then(
                getAllUsersSuccess
            );
        }

        function getAllUsersSuccess(response) {
            return response.data;
        }

        function update() {
            var cookie = Cookies.get();

            userdata.isLoading = true;
//            userdata.updateSuccessfull = false;

            angular.forEach(data, function(v, k) {
                cookie[k] = data[k];
            });

            Cookies.set(cookie);
            return updateDB(cookie);
        }

        function updateDB(cookie) {
            return $http.put('/api/department/' + cookie.department.id +
                    '/user/' + cookie.username + '/', {
                first_name: data.first_name,
                last_name: data.last_name,
                middle_name: data.middle_name,
                email: data.email,
                password: data.password,
                confirm_password: data.confirm_password,
            })
            .then(updateSuccess)
            .catch(updateFailed);
        }

        function updateSuccess(response) {
            userdata.isLoading = false;
//            userdata.updateSuccessfull = true;

//                userdata.updateSuccessfull = false;

//                console.log('Data from update: %s', JSON.stringify(response.data));
//                console.log('Status from update: %s', response.status);
            return response.data;
        }

        function updateFailed(e) {
            return $q.reject(e);
        }
    }
})();
