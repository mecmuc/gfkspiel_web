#!/bin/bash

log_dir=/var/log/gfkspiel.de
server_dir=/var/local/gfk-spiel.de/gfkspiel2/web
nvm_dir=/var/local/gfk-spiel.de/nvm

if [ "$1" = "start" ]; then
    source $nvm_dir/nvm.sh
    nvm use 12
    cd $server_dir
    forever start --append -l $log_dir/forever.log -o $log_dir/server.log -e $log_dir/server.log --pidFile=$server_dir/server.pid --sourceDir=$server_dir server.js --mode=prod

elif [ "$1" = "stop" ]; then
    source $nvm_dir/nvm.sh
    nvm use 12
    cd $server_dir
    forever stop server.js

elif [ "$1" = "restart" ]; then
    source $nvm_dir/nvm.sh
    nvm use 12
    cd $server_dir
    forever restart server.js

elif [ "$1" = "list" ]; then
    source $nvm_dir/nvm.sh
    nvm use 12
    cd $server_dir
    forever list

elif [ "$1" = "update" ]; then
    cd /var/local/gfkspiel.de/gfkspiel2
    git pull
    source $nvm_dir/nvm.sh
    nvm use 12
    cd $server_dir
    npm install
    grunt build

elif [ "$1" = "setup" ]; then
    cd /var/local/gfkspiel.de
    git clone git@bitbucket.org:Koblaid/gfkspiel2.git
    npm install forever -g
    cd gfkspiel2/web
    npm install

else
    echo "Start with one of (start|stop|restart|list|update|setup) as second argument"

fi