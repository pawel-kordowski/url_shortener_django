#!/bin/sh
./utils/wait-for db:5432
./utils/wait-for redis:6379
python manage.py migrate
$@