#!/usr/bin/env bash

cd /opt/apps/local_mingle_backend
git pull origin master
source /root/.virtualenvs/localmingle/bin/activate
pip install -r /opt/apps/local_mingle_backend/requirements.txt
/root/.virtualenvs/localmingle/bin/python manage.py migrate
/root/.virtualenvs/localmingle/bin/python manage.py collectstatic --noinput
sudo supervisorctl stop localmingle
kill $(lsof -t -i:8003)
sudo supervisorctl start localmingle
