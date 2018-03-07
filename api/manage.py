import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import db, create_app
from app.video.models import Video, association_table, Statistic
from app.channel.models import Channel
from app.tags.models import Tag
from app.common.crons.scrape import YoutubeChannelScrapeJob
from app.common.crons.clean_statistics import CleanStatisticsJob

app = create_app(config_name=os.getenv('APP_SETTINGS'))
migrate = Migrate(app, db)
manager = Manager(app)

# adding manager command for migrating database
manager.add_command('db', MigrateCommand)


@manager.command
def seed():
    """Mehtod for adding hardcoded channel"""
    channel = Channel.query.filter(Channel.id == "UCMfPBtm9CWGswAXohT5MFyQ").first()
    if not channel:
        db.session.add(Channel(name='Laisvės TV', id="UCMfPBtm9CWGswAXohT5MFyQ"))
        db.session.commit()


@manager.command
def clean():
    """Mehtod for running Statistic table cleaning job"""
    CleanStatisticsJob.run()


@manager.command
def scrape():
    """Manager command for scrape channels videos"""
    YoutubeChannelScrapeJob(app.config).run()


if __name__ == '__main__':
    manager.run()
