module.exports = function (grunt) {
    grunt.initConfig({
        autoprefixer: {
            dist: {
                files: {
                    'cfp/static/css/prefix-style.css': 'cfp/static/css/style.css'
                }
            }
        },
        watch: {
            styles: {
                files: ['cfp/static/css/style.css'],
                tasks: ['autoprefixer']
            }
        }
    });
    grunt.loadNpmTasks('grunt-autoprefixer');
    grunt.loadNpmTasks('grunt-contrib-watch');
};
