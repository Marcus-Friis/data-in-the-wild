# youtubecommentgetter.py
# By Andreas Belsager, Mads Høgenhaug, Marcus Friis & Mia Pugholm
from youtube_api.youtubegetter import YoutubeGetter
from youtube_api.utilities import timeout
import pandas as pd


class YoutubeCommentGetter(YoutubeGetter):
    def __init__(self, key_gen):
        super().__init__(key_gen)
        self._responses = []
        self.cols = ['channelId', 'videoId', 'commentId', 'textOriginal', 'likeCount', 'publishedAt']
        self.df = self.init_dataframe()

    def get_comments(self, video_id):
        params = {
            'part': 'id,snippet',
            'videoId': video_id
        }

        response = self.get_comments_page(params)
        self._responses.append(response)
        self.add_response_to_dataframe(response)

        try:
            token = response['nextPageToken']
        except KeyError:
            token = False

        while token:
            params['pageToken'] = token
            response = self.get_comments_page(params)
            self.add_response_to_dataframe(response)
            self._responses.append(response)

            try:
                token = response['nextPageToken']
            except KeyError:
                token = False

    def get_comments_page(self, params):
        @timeout
        @self.max_requests_handling
        def wrapper():
            request = self.youtube.search().list(params)
            response = request.execute()

            return response
        return wrapper()

    def add_response_to_dataframe(self, response):
        page_row = {col: [] for col in self.cols}
        for item in response['items']:
            page_row['channelId'].append(item['snippet']['channelId'])
            page_row['videoId'].append(item['snippet']['videoId'])
            page_row['commentId'].append(item['id']['commentId'])
            page_row['textOriginal'].append(item['snippet']['textOriginal'])
            page_row['likeCount'].append(item['snippet']['likeCount'])
            page_row['publishedAt'].append(item['snippet']['publishedAt'])
        df_page = pd.DataFrame(page_row)

        self.df = pd.concat((self.df, df_page), ignore_index=True)