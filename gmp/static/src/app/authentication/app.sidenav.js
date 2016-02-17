(function() {
    angular
        .module('app.sidenav')
        .controller('SidenavController', SidenavController);

    SidenavController.$inject = ['Authentication'];

    function SidenavController(Authentication) {
        var vm = this;

        var data = Authentication.getAuthenticatedAccount();
        console.log('SidenavController cookie: ' + JSON.stringify(data));
        if (data !== undefined) {
            vm.userdata = {
                email: data.email,
                username: data.username,
                department: data.department
            };
        }
        console.log('SidenavController vm.userdata is ' + JSON.stringify(vm.userdata));
    }
})();
