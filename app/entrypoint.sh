#!/bin/bash
/usr/bin/crontab /etc/cron.d/crontab
cron
gunicorn --bind 0.0.0.0:8080 --timeout 500 --log-level=DEBUG --workers 4 app.guni:app