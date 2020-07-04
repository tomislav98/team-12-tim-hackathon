#!/usr/bin/env bash
rm /tmp/*
echo "/db/${APP_NAME_DB}" > "database_path"
python manage.py migrate
python manage.py runserver 0.0.0.0:$APP_PORT
