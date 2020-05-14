#!/bin/bash

docker-compose up -d
sleep 10s
docker-compose exec app /home/api/env/bin/python /home/api/backend/manage.py scrape
