#!/bin/bash
# entrypoint for Render deployment
# ensures migrations and static files are handled before starting server

set -e



# apply database migrations
python manage.py migrate --noinput

# collect static files
python manage.py collectstatic --noinput

# create a default organization/questions if none exist
python manage.py seed || true

# run Gunicorn
exec gunicorn pdif_project.wsgi:application --bind 0.0.0.0:$PORT
