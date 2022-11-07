import googleapiclient.discovery


class YoutubeGetter:
    def __init__(self, youtube):
        self.youtube = youtube

    @staticmethod
    def setup_youtube_api(DEVELOPER_KEY):
        # API information
        api_service_name = "youtube"
        api_version = "v3"

        # API client
        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey=DEVELOPER_KEY)
        return youtube

    def add_response_to_dataframe(self, response):
        pass

    def init_dataframe(self):
        pass


