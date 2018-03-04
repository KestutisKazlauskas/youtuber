import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import db, create_app
from app.video.models import Video, association_table
from app.chennel.models import Channel
from app.tags.models import Tag
from app.common.crons.scrape import YoutubeChannelScrapeJob

app = create_app(config_name=os.getenv('APP_SETTINGS'))
migrate = Migrate(app, db)
manager = Manager(app)

# adding manager command for migrating database
manager.add_command('db', MigrateCommand)


@manager.command
def channel_scrape():
    """Manager command for scrape channels videos"""

    YoutubeChannelScrapeJob(app.config).run()


if __name__ == '__main__':
    manager.run()
