import pandas as pd

from youtube_api.youtubegetter import YoutubeGetter
from youtube_api.utilities import timeout


class YoutubeVideoGetter(YoutubeGetter):
    """
    Class for getting YouTube videos.
    Inherits methods from YoutubeGetter
    """
    def __init__(self, key_gen):
        super().__init__(key_gen)
        self._responses = []  # list of responses for debugging purposes
        self.cols = ['channelId', 'videoId', 'videoTitle', 'publishTime', 'publishedAt']  # overwrite cols from parent
        self.df = self.init_dataframe()  # initialize dataframe on instantiation

    def get_videos(self, channel_id, q='trailer', max_requests=100):
        """
        Executes do-while loop for getting responses from YouTube API and adding them to the classes internal dataframe
        until there are no more page tokens or the max requests limit is hit.
        :param channel_id: YouTube channel ID to scrape videos from
        :param q: Query for the YouTube search
        :param max_requests: Maximum number of requests before stopping scraping
        :return:
        """

        # request parameters for the API
        params = {
            'part': 'id,snippet',
            'type': 'video',
            'channelId': channel_id,
            'q': q
        }

        # do while get responses and add them to dataframe until break condition is met
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
        """
        Get a single response page from YouTube API

        :param params: dict object parsed as **kwargs to api
        :return: response object from api
        """
        @self.max_requests_handling
        def wrapper():
            # search according to params
            request = self.youtube.search().list(**params)

            # Query execution
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
            page_row['channelId'].append(item['snippet']['channelId'])
            page_row['videoId'].append(item['id']['videoId'])
            page_row['videoTitle'].append(item['snippet']['title'])
            page_row['publishTime'].append(item['snippet']['publishTime'])
            page_row['publishedAt'].append(item['snippet']['publishedAt'])
        df_page = pd.DataFrame(page_row)

        self.df = pd.concat((self.df, df_page), ignore_index=True)
