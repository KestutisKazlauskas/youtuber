from datetime import datetime
from googleapiclient.discovery import build


class YouTubeApi:
    """ Helper class for querying youtube api"""

    YOUTUBE_API_SERVICE_NAME = 'youtube'
    YOUTUBE_API_VERSION = 'v3'

    date_format = '%Y-%m-%dT%H:%M:%S.%fZ'

    def __init__(self, api_key):
        self.API_KEY = api_key
        self.youtube_client = build(
            self.YOUTUBE_API_SERVICE_NAME,
            self.YOUTUBE_API_VERSION,
            developerKey=self.API_KEY
        )

        # Initial value for pages looping
        self.next_channel_page = True
        self.channel_pages = 1
        self.next_video_page = True
        self.video_pages = 1

    @staticmethod
    def _count_pages(api_page_info):
        """Method for counting pages of the youtube api results"""

        total = api_page_info.get('totalResults')
        per_page = api_page_info.get('resultsPerPage')

        return int(total/per_page)

    def _set_page_info(self, type, api_response):
        """Method for setting next page info for channel/video api request"""

        # Set next page token
        attribute = 'next_%s_page' % type
        setattr(self, attribute, api_response.get('nextPageToken'))

        # count results pages
        attribute = '%s_pages' % type
        setattr(self, attribute, self._count_pages(api_response['pageInfo']))

    def find_channel_videos(self, channel_id, limit=50, page_token=None):
        """Method for fetching chennel videos ids"""
        response = self.youtube_client.search().list(
            part='id,snippet',
            channelId=channel_id,
            maxResults=limit,
            pageToken=page_token
        ).execute()

        self._set_page_info('channel', response)

        videos = []
        for item in response.get('items', []):
            if item['id']['kind'] == 'youtube#video':
                videos.append(item['id']['videoId'])

        return videos

    def get_videos_stats(self, video_ids, limit=50, page_token=None):
        """Method for getting statistics of the videos"""
        response = self.youtube_client.videos().list(
            part='id,statistics,snippet',
            id=','.join(video_ids),
            maxResults=limit,
            pageToken=page_token
        ).execute()

        self._set_page_info('video', response)

        videos = []
        for item in response.get('items', []):
            videos.append(
                {
                    'youtube_id': item['id'],
                    'name': item['snippet']['title'],
                    'tags': item['snippet']['tags'],
                    'published': datetime.strptime(
                        item['snippet']['publishedAt'], self.date_format
                    ),
                    'views': item['statistics']['viewCount']
                }
            )

        return videos
