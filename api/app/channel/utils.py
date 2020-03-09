import csv
from typing import List
from sqlalchemy.dialects.mysql import insert

from app import db
from app.channel.models import Channel


class ChanelImportCSV:
    @staticmethod
    def _get_data_from_csv(file_path: str) -> list:
        data = []
        with open(file_path, "r", encoding='utf_8') as _csv:
            reader = csv.DictReader(_csv)
            for row in reader:
                if "channel/" in row["channel_url"]:
                    data.append({
                        "name": row["Name"].encode('ascii', 'ignore'),
                        "url": row["channel_url"].replace(
                            "/channel/", ""
                        ).encode('ascii', 'ignore')
                    })

        return data

    @staticmethod
    def _insert_to_database(channels: List[dict]):
        for channel in channels:
            query = insert(Channel).prefix_with('IGNORE').values(
                id=channel["url"],
                name=channel["name"]
            )
            db.session.execute(query)
        db.session.commit()

    def read(self, file_path=None):
        channels = self._get_data_from_csv(file_path)
        self._insert_to_database(channels)

