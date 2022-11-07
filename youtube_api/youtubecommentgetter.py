from youtube_api.youtubegetter import YoutubeGetter
from youtube_api.utilities import timeout


class YoutubeCommentGetter(YoutubeGetter):
    def __init__(self, youtube, video):
        super().__init__(youtube)
        self.video = video
        self.comments = []

    def get_comments(self, videoId):
        params = {
            'part': 'id,snippet',
            'videoId': videoId
        }

        self.get_comments_page(params)


    def get_comments_page(self, params):
        request = self.youtube.search().list(params)

        response = request.execute()

        pass
