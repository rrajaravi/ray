#!/usr/bin/env sh

pkill -f "manage.py runserver"
pkill -f "scrapyd"

if [[ $1 =~ ^d.* ]];
then
    docker-compose down
else
    docker-compose stop 
fi
