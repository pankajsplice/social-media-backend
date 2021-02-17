#!/usr/bin/env bash

cd /opt/apps/ducis_api/
git pull origin master
source /home/admin/.virtualenvs/ducis_api/bin/activate
pip install -r /opt/apps/ducis_api/requirements.txt
/home/admin/.virtualenvs/ducis_api/bin/python manage.py migrate_schemas --shared
/home/admin/.virtualenvs/ducis_api/bin/python manage.py collectstatic --noinput
sudo supervisorctl stop ducis_api
kill $(lsof -t -i:8000)
sudo supervisorctl start ducis_api
