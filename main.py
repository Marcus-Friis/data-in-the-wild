import googleapiclient.discovery
import configparser
from pprint import pprint
import pandas as pd
import numpy as np


class YoutubeGetter:
    def __init__(self, youtube):
        self.youtube = youtube

    def setup_youtube_api(self):
        pass


class YoutubeVideoGetter(YoutubeGetter):
    def __init__(self, youtube):
        super().__init__(youtube)
        self.videos = []

    def get_videos(self):
        pass


class YoutubeCommentGetter(YoutubeGetter):
    def __init__(self, youtube, video):
        super().__init__(youtube)
        self.video = video
        self.comments = []

    def get_comments(self):
        pass


def get_youtube_api_key(filename):
    config = configparser.ConfigParser()
    config.read(filename)
    section = config['DEFAULT']
    for key_string in list(section):
        key = section[key_string]
        yield key


def setup_youtube_api(DEVELOPER_KEY):
    # API information
    api_service_name = "youtube"
    api_version = "v3"

    # API client
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)
    return youtube


if __name__ == '__main__':
    for key in get_youtube_api_key('config.ini'):
        print(key)
        youtube = setup_youtube_api(key)
        ydg = YoutubeVideoGetter(youtube)
