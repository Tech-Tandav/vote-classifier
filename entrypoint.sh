#!/bin/sh
set -e

echo "Running migrations..."
python manage.py migrate

echo "Creating superuser (if not exists)..."

python manage.py create_admin || true
python manage.py import_csv || true
python manage.py load_surname_mapping || true

echo "Starting server..."
exec "$@"
