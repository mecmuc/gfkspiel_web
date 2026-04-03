var express =           require('express');
var fs =                require('fs');
var winston =           require('winston');
var winstonMail =       require('winston-mail');
var expressWinston =    require('express-winston');
var commander =         require('commander');

var db = require('../www/js/dbAccess.js');

commander.option('-m, --mode <mode>', 'Mode of the web server <devel, prod>', 'devel');
commander.parse(process.argv);

var config = {mode: commander.mode};

if (config.mode == 'devel'){
    config.port = 3000;
    config.gameLogPath = 'game.log';
    config.logMode = 'dev';
    config.indexHtmlName = 'index_devel.html';
    config.cacheExpiration = 0;
    config.staticDir = 'static_devel';

} else if (config.mode == 'prod'){
    config.port = 3000;
    config.gameLogPath = '/var/log/gfkspiel.de/game.log';
    config.logMode = 'default';
    config.indexHtmlName = 'index_prod.html';
    config.cacheExpiration = 60*60*24*365*1000; // 1000 years, resources will be reloaded if their etag changes;
    config.staticDir = 'static_prod';

} else {
    console.log("error: option '-m, --mode <mode>' must be 'devel' or 'prod'");
    process.exit(0);
}


var googleAnalytics = "<script type=\"text/javascript\">var _gaq = _gaq || [];_gaq.push(['_setAccount', 'UA-42706997-1']);_gaq.push(['_trackPageview']);(function() {var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);})();</script>";

var app = express();


var gameLogger = new winston.Logger({
    transports: [new winston.transports.File({ filename: config.gameLogPath })]
});

app.use(express.logger(config.logMode));
app.use(express.compress());
app.use(express.favicon(config.staticDir+'/img/favicon.ico'));
app.use(express.bodyParser());

app.use('/ajax', function(req, res, next){
    var methodName = req.path.substring(1);
    if (methodName in db.DbAccess){
        var jsonArgs = req.body;

        var callback = function(err, resultObj){
            if (err){
                console.log(err);
                console.log(jsonArgs);
                res.status(500);
                res.send(err);
            } else {
                res.json(resultObj);
            }
        };
        db.DbAccess[methodName](jsonArgs, callback);
        gameLogger.log('info', 'AJAX', {method: methodName, remoteAddr: req.ip, args: jsonArgs});
    } else {
        res.status(404);
        res.send('Page not found');
    }
});

app.use('/', function(req, res, next){
    if (req.path != '/' && req.path != '/index.html'){
        next();
        return;
    }
    fs.readFile(config.indexHtmlName, 'utf8', function(err, index_file_content) {
        if (err) {throw err;}
        fs.readFile('../www/html/index_body.html', 'utf8', function(err, body_file_content) {
            if (err) {throw err;}
            res.setHeader('Cache-Control', 'public, max-age=' + config.cacheExpiration);
            var index = index_file_content.replace('%(body)s', body_file_content).replace('%(googleanalytics)s', googleAnalytics);
            res.send(index);
        });
    });
    gameLogger.log('info', 'INDEX', {remoteAddr: req.ip});
});

app.use(express.static(__dirname + '/' + config.staticDir, { maxAge: config.cacheExpiration }));
app.use('/audio', express.static(__dirname + '/../audio', { maxAge: config.cacheExpiration }));

if (config.mode == 'prod'){
    var mailTransport = new winstonMail.Mail({
        ssl: true,
        host:     'smtp.gmail.com',
        username: 'gfkspiel.de@gmail.com',
        password: 'bJk153xyz258kxg827',
        from:     'gfkspiel.de@gmail.com',
        to:       'gfkspiel@gmail.com'
    });
    mailTransport.on('error', function (err) { console.log('Error sending the error mail', err );});
    app.use(expressWinston.errorLogger({ transports: [mailTransport] }));
}

console.log('Starting server in mode "'+ commander.mode+'" on port ' + config.port + '...');
app.listen(config.port, function(err){
    if (err) {
        return console.log('Error while trying to listen to port '+config.port+': '+err);
    }

    // Switch the user of the process after the socket is opened
    // http://syskall.com/dont-run-node-dot-js-as-root/

    // Set the group id
    var gid = parseInt(process.env.SUDO_GID, 10);
    if (gid) {
        process.setgid(gid);
        console.log('Servers GID is now ' + process.getgid());
    } else {
        console.log('GID was not changed');
    }

    // Set the user id
    var uid = parseInt(process.env.SUDO_UID, 10);
    if (uid) {
        process.setuid(uid);
        console.log('Servers UID is now ' + process.getuid());
    } else {
        console.log('GID was not changed');
    }
});
