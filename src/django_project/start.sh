#! /bin/bash

# Start gunicorn Process
echo Starting Gunicorn.
exec gunicorn django_project.wsgi:application \
	--bind 0.0.0.0:8000 \
	--workers 3
