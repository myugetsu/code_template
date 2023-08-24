#!/bin/sh
# while true; do
#     flask db init
#     flask db migrate
#     flask db upgrade
#     if [[ "$?" == "0" ]]; then
#         break
#     fi
#     echo Upgrade command failed, retrying in 5 secs...
#     sleep 5
# done
flask db init
flask db migrate
flask db upgrade
flask translate compile
exec gunicorn -b :5000 --access-logfile - --error-logfile - flask_new:app
