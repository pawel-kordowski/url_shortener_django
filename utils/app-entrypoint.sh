#!/bin/sh
./utils/wait-for db:5432
python manage.py migrate
$@