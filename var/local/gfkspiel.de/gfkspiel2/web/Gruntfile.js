module.exports = function(grunt) {

    // Project configuration.
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        concat: {
            options: {
                separator: ';'
            },
            dist: {
                src: ['../www/js/app.js', '../www/js/adapterWeb.js'],
                dest: '../tmp/<%= pkg.name %>.js'
            }
        },

        uglify: {
            options: {
                banner: '/*! <%= pkg.name %> */\n',
                mangle: true,
                report: 'min',
            },
            dist: {
                src: ['<%= concat.dist.dest %>'],
                dest: 'static_prod/js/<%= pkg.name %>.min.js',
            }
        },

        cssmin: {
            options: {
                banner: '/*! <%= pkg.name %> */\n',
                report: 'min',
            },
            dist: {
                src: ['../www/css/gfkspiel.css'],
                dest: 'static_prod/css/<%= pkg.name %>.min.css',
            }
        },

        jshint: {
            options: {
                curly: true,
                indent: 4,
                latedef: true,
                trailing: true,
                unused: 'vars',
                undef: true
            },
            browser: {
                options: {
                    browser: true,
                    jquery: true,
                    globals: {
                        DbAccess: false,
                        adapter: true,
                        store: false,
                        alert: false,
                    }
                },
                files: {
                    src: ['../www/js/adapterCordova.js', '../www/js/adapterWeb.js', '../www/js/app.js']
                }
            },
            node: {
                options: {
                    node: true,
                },
                files: {
                    src: ['adapterNode.js', 'server.js', 'Gruntfile.js', '../www/js/dbAccess.js']
                }
            }
        },

        githooks: {
            all: {
                options: {
                    dest: '../.git/hooks',
                    template: 'githooks-template.hb',
                },
                'pre-commit': 'jshint',
            }
        },


        watch: {
            files: ['**/*'],
            tasks: ['jshint'],
        },

        csslint: {
            src: ['../www/css/gfkspiel.css']
        }
    });

    grunt.loadNpmTasks('grunt-contrib-jshint');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks('grunt-githooks');
    grunt.loadNpmTasks('grunt-contrib-cssmin');
    grunt.loadNpmTasks('grunt-contrib-csslint');


    // Default task(s).
    grunt.registerTask('default', ['watch']);
    grunt.registerTask('build', ['concat', 'uglify', 'cssmin']);

};
