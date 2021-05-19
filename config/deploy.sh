#!/usr/bin/env bash

cd /opt/apps/local_mingle_backend
git pull origin master
source /home/admin/.virtualenvs/local_mingle_backend/bin/activate
pip install -r /opt/apps/local_mingle_backend/requirements.txt
/home/admin/.virtualenvs/local_mingle_backend/bin/python manage.py migrate
/home/admin/.virtualenvs/local_mingle_backend/bin/python manage.py collectstatic --noinput
sudo supervisorctl stop local_mingle_backend
kill $(lsof -t -i:8003)
sudo supervisorctl start local_mingle_backend
