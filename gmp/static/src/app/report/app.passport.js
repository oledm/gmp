(function() {
    'use strict';

    angular
        .module('app.passport')
        .controller('PassportController', PassportController);

    PassportController.$inject = ['UserData', 'Department'];
    function PassportController(UserData, Department) {
        var vm = this,
            ranks = [
                'руководитель бригады',
                'зам. руководителя бригады',
                'член бригады'
            ],
	    measurers = {
		all: Department.measurers(),
		selected: [],
                sortOrder: 'name'
	    };

        vm.addEmployee = addEmployee;
        vm.allEmployees = [];
        vm.measurers = measurers;
        vm.ranks = ranks;
        vm.team = [{'name': '', 'required': 'required'}];

        activate();

        //////////////////////////

        function activate() {
            getEmployees();
        }

        function addEmployee() {
//            console.log('team: ' + JSON.stringify(vm.team));
            vm.team.push({
                'name': ''
            });
        }

        function getEmployees() {
            UserData.getAllUsers()
                .then(function(data) {
                    vm.allEmployees = data;
                });
        }
    }
})();
