import googleapiclient.discovery
import googleapiclient
import pandas as pd


class YoutubeGetter:
    """
    Parent class for collecting data from YouTube.
    Inherited by YoutubeVideoGetter and YoutubeCommentGetter
    """
    def __init__(self, key_gen):
        self.key_gen = key_gen
        self.key = next(self.key_gen)
        self.youtube = self.setup_youtube_api(self.key)
        self.cols = []
        self.df = self.init_dataframe()

    @staticmethod
    def setup_youtube_api(DEVELOPER_KEY):
        """
        Sets up youtube connection with parsed key
        :param DEVELOPER_KEY: YouTube API key
        :return: youtube api client
        """
        # API information
        api_service_name = "youtube"
        api_version = "v3"

        # API client
        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey=DEVELOPER_KEY)
        return youtube

    def max_requests_handling(self, func):
        """
        Decorator method for changing API keys when a key runs out of credits.
        Apply to methods that make API calls
        :param func: decorated method
        :return: wrapper func
        """
        def wrapper(*args, **kwargs):
            # while keys are available
            while True:
                # execute parsed function
                try:
                    out = func(*args, **kwargs)
                    return out
                # if google api error is raised, iterate to next api key
                except googleapiclient.errors.HttpError as e:
                    try:
                        self.key = next(self.key_gen)
                        self.youtube = self.setup_youtube_api(self.key)
                        print(f'getting new key:\t\t{self.key}')
                    # if there are no more keys, raise appropriate error
                    except StopIteration:
                        raise e
        return wrapper

    def add_response_to_dataframe(self, response):
        """
        Abstract method for adding a get response to dataframe
        """
        pass

    def init_dataframe(self):
        """
        Method for initializing pandas dataframe
        :return: pd.DataFrame with needed columns
        """
        df = pd.DataFrame(columns=self.cols)
        return df

    def reset_dataframe(self):
        """
        Re-initialize dataframe
        """
        self.df = self.init_dataframe()
