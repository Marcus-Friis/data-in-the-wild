# youtubecommentgetter.py
# By Andreas Belsager, Mads Høgenhaug, Marcus Friis & Mia Pugholm
import googleapiclient.errors

from youtube_api.youtubegetter import YoutubeGetter
from youtube_api.utilities import timeout
import pandas as pd


class YoutubeCommentGetter(YoutubeGetter):
    def __init__(self, key_gen):
        super().__init__(key_gen)
        self._responses = []
        self.cols = ['videoId', 'commentId', 'textOriginal', 'likeCount', 'publishedAt']
        self.df = self.init_dataframe()

    def get_comments(self, video_id, max_requests=100):
        params = {
            'part': 'id,snippet',
            'videoId': video_id
        }

        token_iterator = 0
        while True:
            response = self.get_comments_page(params)
            if response is None:
                break

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

    def get_comments_page(self, params):
        @timeout
        @self.max_requests_handling
        @self.comments_disabled_handler
        def wrapper():
            request = self.youtube.commentThreads().list(**params)
            response = request.execute()

            return response
        return wrapper()

    def add_response_to_dataframe(self, response):
        page_row = {col: [] for col in self.cols}
        for item in response['items']:
            page_row['videoId'].append(item['snippet']['videoId'])
            page_row['commentId'].append(item['id'])
            page_row['textOriginal'].append(item['snippet']['topLevelComment']['snippet']['textOriginal'])
            page_row['likeCount'].append(item['snippet']['topLevelComment']['snippet']['likeCount'])
            page_row['publishedAt'].append(item['snippet']['topLevelComment']['snippet']['publishedAt'])
        df_page = pd.DataFrame(page_row)

        self.df = pd.concat((self.df, df_page), ignore_index=True)

    @staticmethod
    def comments_disabled_handler(func):
        def wrapper(*args, **kwargs):
            try:
                out = func(*args, **kwargs)
                return out
            except googleapiclient.errors.HttpError as e:
                if 'has disabled comments' in str(e):
                    print('disabled comments')
                else:
                    raise e
        return wrapper
