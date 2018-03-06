import datetime
from dateutil.relativedelta import relativedelta
from app.video.models import Statistic
from app import db


class CleanStatisticsJob:
    """
    class for clean older then one month video statistic records in the db.
    CronJob runs every week on sunday 23  hour (0 23 * * 0)
    """
    @staticmethod
    def run():
        """Method for running cronjob"""
        date = datetime.date.today() - relativedelta(months=1)
        db.session.query(Statistic).filter(Statistic.time_created < date).delete()
        db.session.commit()


