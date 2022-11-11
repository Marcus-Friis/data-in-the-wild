from youtube_api.youtubegetter import YoutubeGetter
from youtube_api.utilities import timeout


class YoutubeCommentGetter(YoutubeGetter):
    def __init__(self, youtube):
        super().__init__(youtube)
        self._responses = []
        self.cols = ['videoId', 'textOriginal', 'publishedAt']
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
    @timeout
    def get_comments_page(self, params):
        request = self.youtube.search().list(params)
        response = request.execute()

        return response

    def add_response_to_dataframe(self, response):
        page_row = {col: [] for col in self.cols}
        for item in response['items']:
            page_row['textOriginal'].append(item['snippet']['textOriginal'])
            page_row['publishedAt'].append(item['snippet']['publishedAt'])
            pass