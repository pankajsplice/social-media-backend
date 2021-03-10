#!/usr/bin/env bash

cd /opt/apps/pwa-event/
git pull origin master
source /root/.virtualenvs/pwaevent/bin/activate
pip install -r /opt/apps/pwa-event/requirements.txt
/root/.virtualenvs/pwaevent/bin/python manage.py migrate
/root/.virtualenvs/pwaevent/bin/python manage.py collectstatic --noinput
sudo supervisorctl stop pwaevent
kill $(lsof -t -i:8001)
sudo supervisorctl start pwaevent
