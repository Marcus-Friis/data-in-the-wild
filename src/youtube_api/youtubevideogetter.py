# youtubevideogetter.py
# By Andreas Belsager, Mads Høgenhaug, Marcus Friis & Mia Pugholm
import pandas as pd

from youtube_api.youtubegetter import YoutubeGetter
from youtube_api.utilities import timeout


class YoutubeVideoGetter(YoutubeGetter):
    def __init__(self, key_gen):
        super().__init__(key_gen)
        self._responses = []
        self.cols = ['channelId', 'videoId', 'videoTitle', 'publishTime', 'publishedAt']
        self.df = self.init_dataframe()

    def get_videos(self, channel_id, q='trailer', max_requests=100):
        params = {
            'part': 'id,snippet',
            'type': 'video',
            'channelId': channel_id,
            'q': q
        }

        token_iterator = 0
        while True:
            response = self.get_video_page(params)
            self._responses.append(response)
            self.add_response_to_dataframe(response)

            try:
                token = response['nextPageToken']
                params['pageToken'] = token
            except KeyError:
                token = False

            if not (token and token_iterator < max_requests):
                break

            token_iterator += 1

    def get_video_page(self, params):
        # @timeout
        @self.max_requests_handling
        def wrapper():
            request = self.youtube.search().list(**params)

            # Query execution
            response = request.execute()
            return response
        return wrapper()

    def add_response_to_dataframe(self, response):
        page_row = {col: [] for col in self.cols}
        for item in response['items']:
            page_row['channelId'].append(item['snippet']['channelId'])
            page_row['videoId'].append(item['id']['videoId'])
            page_row['videoTitle'].append(item['snippet']['title'])
            page_row['publishTime'].append(item['snippet']['publishTime'])
            page_row['publishedAt'].append(item['snippet']['publishedAt'])
        df_page = pd.DataFrame(page_row)

        self.df = pd.concat((self.df, df_page), ignore_index=True)
