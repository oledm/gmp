(function() {
    'use strict';

    angular
        .module('app.userdata.service')
        .factory('UserData', UserData);

    function UserData() {
        var data = {
            email: '',
            first_name: '',
            last_name: '',
            department: ''
        };

//        console.log('Current UserData is ' + data);

        return data;
    }
})();
