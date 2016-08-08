var gulp = require('gulp');
var concat = require('gulp-concat');
var sass = require('gulp-sass');
var uglify = require('gulp-uglify');
var babel = require('gulp-babel');
var ngAnnotate = require('gulp-ng-annotate')
var sourcemaps = require('gulp-sourcemaps')
var templateCache = require('gulp-angular-templatecache');
//var sleep = require('sleep');
var exec = require('gulp-exec');
exec = require('child_process').exec;

 

gulp.task('templates', () => {
    gulp.src('gmp/static/src/app/**/*.tpl.html')
        .pipe(templateCache('templates.js', {module: 'app'}))
        .pipe(gulp.dest('gmp/static/dist'));
});

gulp.task('sass', () => {
    gulp.src('gmp/static/src/sass/**/*.scss')
        .pipe(sass().on('error', sass.logError))
        .pipe(gulp.dest('gmp/static/dist'));
});


gulp.task('js', () => {
    gulp.src(['gmp/static/src/app/**/*.module.js',
              'gmp/static/src/app/**/*.js'])
        .pipe(sourcemaps.init())
            .pipe(concat('app.min.js'))
            .pipe(babel({
                presets: ['es2015']
            }))
            .pipe(ngAnnotate())
            .pipe(uglify())
        .pipe(sourcemaps.write())
        .pipe(gulp.dest('gmp/static/dist'));
});

//gulp.task('report', function() {
//    sleep.usleep(1500000);
//    exec('curl "http://127.0.0.1:8000/report/" > ~/passport.pdf && ' + 
//         'chromium ~/passport.pdf');
//});

gulp.task('build', ['js', 'templates', 'sass']);

gulp.task('watch-report', ['report'], () => {
    gulp.watch('gmp/**/*.py', ['report']);
});

gulp.task('watch', ['js', 'templates', 'sass'], () => {
    gulp.watch('gmp/static/src/app/**/*.js', ['js']);
    gulp.watch('gmp/static/src/app/**/*.tpl.html', ['templates']);
    gulp.watch('gmp/static/src/sass/**/*.scss', ['sass']);
});

gulp.task('default', ['watch'], () => {});
