module.exports = function (grunt) {

  var appConfig = grunt.file.readJSON('package.json');

  // Load grunt tasks automatically
  // see: https://github.com/sindresorhus/load-grunt-tasks
  require('load-grunt-tasks')(grunt);

  // Time how long tasks take. Can help when optimizing build times
  // see: https://npmjs.org/package/time-grunt
  require('time-grunt')(grunt);

  var pathsConfig = function (appName) {
    this.app = appName || appConfig.name;

    return {
      app: this.app,
      templates: this.app + '/templates',
      css: this.app + '/static/src/assets/css',
      sass: this.app + '/static/src/sass',
      fonts: this.app + '/static/fonts',
      images: this.app + '/static/images',
      js: this.app + '/static/src',
      manageScript: 'manage.py',
    }
  };

  grunt.initConfig({

    paths: pathsConfig(),
    pkg: appConfig,

    // see: https://github.com/gruntjs/grunt-contrib-watch

    watch: {
      gruntfile: {
        files: ['Gruntfile.js']
      },
      sass: {
        files: ['<%= paths.sass %>/**/*.{scss,sass}'],
        tasks: ['sass:dev'],
        options: {
          atBegin: true
        }
      },
      python: {
        files: ['<%= paths.app %>/**/*.py'],
        tasks: ['bgShell:runTests'],
      },
      pythonForReport: {
        files: ['<%= paths.app %>/**/*.py'],
        tasks: ['wait', 'bgShell:makeReport'],
      },
      js: {
        files: ['<%= paths.js %>/**/*.js'],
        tasks: ['eslint']
      },
      livereload: {
        files: [
          '<%= paths.js %>/**/*.js',
          '<%= paths.sass %>/**/*.{scss,sass}',
          '<%= paths.app %>/**/*.html'
          ],
        options: {
          spawn: false,
          livereload: true,
        },
      },
    },

    // see: https://github.com/sindresorhus/grunt-sass
    sass: {
      dev: {
          options: {
              outputStyle: 'nested',
              sourceMap: false,
              precision: 10
          },
          files: {
              '<%= paths.css %>/app.css': '<%= paths.sass %>/app.scss'
          },
      },
      dist: {
          options: {
              outputStyle: 'compressed',
              sourceMap: false,
              precision: 10
          },
          files: {
              '<%= paths.css %>/app.css': '<%= paths.sass %>/app.scss'
          },
      }
    },

    //see https://github.com/nDmitry/grunt-postcss
    postcss: {
      options: {
        map: true, // inline sourcemaps

        processors: [
          require('pixrem')(), // add fallbacks for rem units
          require('autoprefixer-core')({browsers: [
            'Android 2.3',
            'Android >= 4',
            'Chrome >= 20',
            'Firefox >= 24',
            'Explorer >= 8',
            'iOS >= 6',
            'Opera >= 12',
            'Safari >= 6'
          ]}), // add vendor prefixes
          require('cssnano')() // minify the result
        ]
      },
      dist: {
        src: '<%= paths.css %>/*.css'
      }
    },

    // https://www.npmjs.com/package/grunt-wait
    wait: {
        options: {
            delay: 1500
        },
        pause: {      
            options: {
                before: function(options) {
                    console.log('pausing %dms', options.delay);
                },
                after: function() {
                    console.log('pause end');
                }
            }
        },
    },

    // see: https://npmjs.org/package/grunt-bg-shell
    bgShell: {
      _defaults: {
        bg: true
      },
      runDjango: {
        cmd: 'python <%= paths.manageScript %> runserver'
      },
      runTests: {
        cmd: 'python <%= paths.manageScript %> test gmp.authentication gmp.filestorage gmp.certificate',
        bg: false
      },
      makeReport: {
        cmd: 'curl "http://127.0.0.1:8000/report/" > ~/passport.pdf && chromium ~/passport.pdf',
        bg: false
      }
      
    },

    eslint: {
        src: ['<%= paths.js %>/**/*.js']
    },

  });

  grunt.registerTask('serve', [
    'bgShell:runDjango',
    'bgShell:runTests',
    'watch'
  ]);


  grunt.registerTask('report', [
    'bgShell:runDjango',
    'wait',
    'bgShell:makeReport',
    'watch:pythonForReport',
  ]);

  grunt.registerTask('build', [
    'sass:dist',
    'eslint',
    'postcss'
  ]);

  grunt.registerTask('default', [
    'serve',
  ]);

};
