import pandas as pd

from youtube_api.youtubegetter import YoutubeGetter
from youtube_api.utilities import max_requests_handling, timeout


class YoutubeVideoGetter(YoutubeGetter):
    def __init__(self, youtube):
        super().__init__(youtube)
        self._responses = []
        self.cols = ['channelId', 'videoId', 'videoTitle', 'publishTime', 'publishedAt']
        self.df = self.init_dataframe()

    def get_all_videos(self, channel_id, q='trailer'):
        params = {
            'part': 'id,snippet',
            'type': 'video',
            'channelId': channel_id,
            'q': q
        }
        response = self.get_video_page(params)
        self._responses.append(response)
        self.add_response_to_dataframe(response)

        try:
            token = response['nextPageToken']
        except KeyError:
            return

        while token:
            params['pageToken'] = token
            response = self.get_video_page(params)
            self.add_response_to_dataframe(response)
            self._responses.append(response)

            try:
                token = response['nextPageToken']
            except KeyError:
                token = False

    @timeout
    def get_video_page(self, params):
        request = self.youtube.search().list(**params)

        # Query execution
        response = request.execute()
        return response

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

    def init_dataframe(self):
        df = pd.DataFrame(columns=self.cols)
        return df

    def reset_dataframe(self):
        self.df = self.init_dataframe()
