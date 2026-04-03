var sqlite3 = require('sqlite3').verbose();

exports.DbAdapter = function(){
    var db = new sqlite3.Database('../database/gfkspiel.db');
    this.select = function(stmt, args, callback){
        db.serialize(function() {
            db.all(stmt, args, callback);
        });
    };
    return this;
};
