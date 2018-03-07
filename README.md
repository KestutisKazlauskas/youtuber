# Youtuber
## About
App that uses Youtube API(https://developers.google.com/youtube/v3/) to scrape channel videos.
Every 20 minutes cron job scan channel and scrapes videos information and statistics and save to database. This time interval was chonsen, this time is enough to count new videos views in first hour. Because of youtube request limitation(1000000 quotas) this time interval let's us scrape a channel with approximately 2000 - 3000 videos and do not exceed a limit of quotas. App uses python3 for scraping. For scrapig results is Rest api. To show results app uses html and js. In the front end we can filter videos by tags, or by its performance.

## Used technologies
- Python3, Flask,  SQLAlchemy, framework for a backend api.
- HTML, CSS, JS for app front-end
- Mysql for a database
- Docker for app running app
- Git for code versioning

## How to start an app
1. Clone the repository:
```python
git clone git@github.com:KestutisKazlauskas/youtuber.git 
```
2. In cloned directory run docker build
```python
docker-compose build
```
3. In cloned directory run command tu start docker containers
```python
sudo docker-compose up -d
```
4. Now you can run front-end and api:
- Videos Api: ```python
http://localhost:5000/api/videos
```
- Video tags api```python
http://localhost:5000/api/tags
```
- Frontend: ```python
http://localhost:8080
```
**Note if using docker on Windows with docker toolbox localhost should be change into docker-machine ip default IP**

## TODO
- Write tests for code
- Add authentication to an ip
- Run api on nginx and uwsgi
- Add api for channels (CRUD). Now are only channel model and seed for one channel fast creation.
- Expaned videos and tags filters
- In case of a lot of channel and videos and their statistics scraping consider a nosql database(mongodb, couchdb) instead of (or with) mysql.
- Code forntend app using js framework such as angularjs or react.js
