FROM debian:9

MAINTAINER kstutisk4@gmail.com

# update packages
RUN apt-get update && apt-get install -y apt-utils nginx cron\
    python3  python3-pip procps vim curl wget libssl-dev build-essential libffi-dev python3-dev \
    python3-setuptools python-dev python3-dev default-libmysqlclient-dev mysql-client \
    libjpeg62-turbo-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev
RUN pip3 install virtualenv


COPY config/start.sh /bin/
RUN chmod 755 /bin/start.sh

# setup the configfiles
ADD . /home/docker/code/
RUN rm /etc/nginx/sites-enabled/default /etc/nginx/nginx.conf
RUN cp /home/docker/code/config/nginx.conf /etc/nginx/
RUN cp /home/docker/code/config/server.conf /etc/nginx/sites-enabled/

# create users
RUN useradd -m api
RUN su api -c 'cd && mkdir backend'
RUN su api -c 'cp -a /home/docker/code/api/. /home/api/backend/'
RUN su api -c 'cp -a /home/docker/code/frontend/. /home/api/frontend/'
RUN su api -c 'cd && virtualenv env'

RUN su api -c '/home/api/env/bin/pip3 install -r /home/api/backend/requirements.txt'

# addin crons
#RUN cp /home/docker/code/config/api-cron /etc/cron.d/api-cron
#RUN crontab /etc/cron.d/api-cron

# Removed settings files
RUN rm -rf /home/docker/code/
