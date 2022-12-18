# youtubegetter.py
# By Andreas Belsager, Mads Høgenhaug, Marcus Friis & Mia Pugholm
import googleapiclient.discovery
import googleapiclient
import pandas as pd


class YoutubeGetter:
    def __init__(self, key_gen):
        self.key_gen = key_gen
        self.key = next(self.key_gen)
        self.youtube = self.setup_youtube_api(self.key)
        self.cols = []
        self.df = self.init_dataframe()

    @staticmethod
    def setup_youtube_api(DEVELOPER_KEY):
        # API information
        api_service_name = "youtube"
        api_version = "v3"

        # API client
        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey=DEVELOPER_KEY)
        return youtube

    def max_requests_handling(self, func):
        def wrapper(*args, **kwargs):
            while True:
                try:
                    out = func(*args, **kwargs)
                    return out
                except googleapiclient.errors.HttpError as e:
                    try:
                        self.key = next(self.key_gen)
                        self.youtube = self.setup_youtube_api(self.key)
                        print(f'getting new key:\t\t{self.key}')
                    except StopIteration:
                        raise e
        return wrapper

    def add_response_to_dataframe(self, response):
        pass

    def init_dataframe(self):
        df = pd.DataFrame(columns=self.cols)
        return df

    def reset_dataframe(self):
        self.df = self.init_dataframe()
