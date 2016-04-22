var gulp = require('gulp');
var concat = require('gulp-concat');
var uglify = require('gulp-uglify');
var ngAnnotate = require('gulp-ng-annotate')
var sourcemaps = require('gulp-sourcemaps')
var templateCache = require('gulp-angular-templatecache');

gulp.task('templates', () => {
    gulp.src('gmp/static/src/app/**/*.tpl.html')
        .pipe(templateCache('templates.js', {module: 'app'}))
        .pipe(gulp.dest('gmp/static/dist'));
});

gulp.task('js', function() {
    gulp.src(['gmp/static/src/app/**/*.module.js',
              'gmp/static/src/app/**/*.js'])
        .pipe(sourcemaps.init())
            .pipe(concat('app.min.js'))
            .pipe(ngAnnotate())
            .pipe(uglify())
        .pipe(sourcemaps.write())
        .pipe(gulp.dest('gmp/static/dist'));
});

gulp.task('build', ['js', 'templates']);

gulp.task('watch', ['js', 'templates'], function() {
    gulp.watch('gmp/static/src/app/**/*.js', ['js']);
    gulp.watch('gmp/static/src/app/**/*.tpl.html', ['templates']);
});

gulp.task('default', ['watch'], function() {
});
