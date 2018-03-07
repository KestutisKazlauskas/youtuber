#!/bin/bash
service nginx start

cd /home/api/backend && /home/api/env/bin/python3 /home/api/backend/manage.py db upgrade
cd /home/api/backend && /home/api/env/bin/python3 /home/api/backend/manage.py seed
cron
/home/api/env/bin/python3 /home/api/backend/run.py
