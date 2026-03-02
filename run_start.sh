#!/bin/bash
# entrypoint for Render deployment
# ensures migrations and static files are handled before starting server

set -e


# Install WeasyPrint system dependencies (for Render.com)
apt-get update
apt-get install -y libpango-1.0-0 libpangocairo-1.0-0 libcairo2 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info

# apply database migrations
python manage.py migrate --noinput

# collect static files
python manage.py collectstatic --noinput

# create a default organization/questions if none exist
python manage.py seed || true

# run Gunicorn
exec gunicorn pdif_project.wsgi:application --bind 0.0.0.0:$PORT
