#!/usr/bin/env sh

if [ -z "$DJANGO_SECRET_KEY" ]; then
    echo "Error: Set variable DJANGO_SECRET_KEY and try again"
    exit 1
fi 

docker-compose up &
sleep 15
cd ray
scrapyd &

mysql="mysql"
$mysql -uroot -h $DB_HOST -p$DB_PASSWORD -e "CREATE DATABASE IF NOT EXISTS localdb CHARACTER SET utf8 COLLATE utf8_unicode_ci;"
$mysql -uroot -h $DB_HOST -p$DB_PASSWORD -e "ALTER DATABASE localdb CHARACTER SET utf8 COLLATE utf8_unicode_ci;"
$mysql -uroot -h $DB_HOST -p$DB_PASSWORD -e "GRANT ALL ON localdb.* TO 'rajaravi'@'%' IDENTIFIED BY 'rajaravi' WITH GRANT OPTION;"

./manage.py collectstatic --no-input
python manage.py migrate
python manage.py shell -c "from django.contrib.auth.models import User; \
                           User.objects.filter(username='rajaravi').exists() or \
                           User.objects.create_superuser(username='rajaravi', email='r.rajaravi@gmai.com', password='rajaravi')"
python manage.py runserver &
