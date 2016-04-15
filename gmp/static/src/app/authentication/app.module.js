(function() {
    'use strict';

    angular.module('app', [
        'app.config',
        'app.authentication',
        'app.department',
        'app.serverdata',
        'app.engine.service',
        'app.main',
        'app.datepicker',
        'app.login',
        'app.register',
        'app.cookies',
        'app.userdata.service',
        'app.userdata.controller',
        'app.toolbar',
        'app.upload',
        'app.upload.service',
        'app.passport',
        'app.passport.service',
        'app.report',
    ]);
})();
