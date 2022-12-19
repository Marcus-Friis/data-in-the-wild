import googleapiclient.errors

from youtube_api.youtubegetter import YoutubeGetter
from youtube_api.utilities import timeout
import pandas as pd


class YoutubeCommentGetter(YoutubeGetter):
    def __init__(self, key_gen):
        super().__init__(key_gen)
        self._responses = []  # list of responses for debugging purposes
        self.cols = ['videoId', 'commentId', 'textOriginal', 'likeCount', 'publishedAt']  # overwrite cols from parent
        self.df = self.init_dataframe()  # initialize dataframe on instantiation

    def get_comments(self, video_id, max_requests=100):
        """
        Executes do-while loop for getting responses from YouTube API and adding them to the classes internal dataframe
        until there are no more page tokens or the max requests limit is hit.
        :param video_id: YouTube video ID to scrape comments from
        :param max_requests: Maximum number of requests before stopping scraping
        :return:
        """

        # request parameters for the API
        params = {
            'part': 'id,snippet',
            'videoId': video_id
        }

        # do while get responses and add them to dataframe until break condition is met
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
        """
        Get a single comment response page.
        :param params: parameters parsed as **kwargs to YouTube's list() method
        :return: comment response object
        """
        @timeout
        @self.max_requests_handling
        @self.comments_disabled_handler
        def wrapper():
            # get comments from specified parameters
            request = self.youtube.commentThreads().list(**params)
            response = request.execute()

            return response
        return wrapper()

    def add_response_to_dataframe(self, response):
        """
        Formats response object and adds it to internal dataframe.
        :param response: Response object from YouTube api
        :return:
        """
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
        """
        Decorator method for handling instances when comments are disabled.
        In short, wraps the input function in try except and passes if comments are disabled.
        :param func: decorated function
        :return:
        """
        def wrapper(*args, **kwargs):
            # execute input function
            try:
                out = func(*args, **kwargs)
                return out
            # if the api throws a google api error and it is due to disabled comments, print so
            except googleapiclient.errors.HttpError as e:
                if 'has disabled comments' in str(e):
                    print('disabled comments')
                else:
                    raise e
        return wrapper
