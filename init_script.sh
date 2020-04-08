#!/bin/bash

nginx
/usr/bin/env gunicorn --chdir /usr/src/app/ infra_dashboard.wsgi:application --timeout 120 --bind 0.0.0.0:90 --workers 3
