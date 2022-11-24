# main.py
# By Andreas Belsager, Mads Høgenhaug, Marcus Friis & Mia Pugholm
import pandas as pd
import requests
import re

from youtube_api.utilities import get_youtube_api_key, setup_youtube_api
from youtube_api.youtubevideogetter import YoutubeVideoGetter
from youtube_api.youtubecommentgetter import YoutubeCommentGetter


def get_scores(id):
    r = requests.get(f"https://returnyoutubedislikeapi.com/votes?videoId={id}")
    txt = r.text

    likes = int(re.findall('(?<="likes":).[0-9]+', txt)[0])
    dislikes = int(re.findall('(?<="dislikes":).[0-9]+', txt)[0])
    views = int(re.findall('(?<="viewCount":).[0-9]+', txt)[0])
    return views, likes, dislikes


if __name__ == '__main__':
    channel_ids = {
        # 'netflix': 'UCWOA1ZGywLbqmigxE4Qlvuw',
        # 'hbo': 'UCx-KWLTKlB83hDI6UKECtJQ'
        # 'amazon': 'UCwSIJCMWZC5GDM59wj7pMsg',
        # 'disney': 'UCIrgJInjLS2BhlHOMDW7v0g'
        # 'elias': 'UC9InaN7Xbh39_tUSCfi-7lQ'
    }

    key_gen = get_youtube_api_key('config.ini')
    ydg = YoutubeVideoGetter(key_gen)

    for key, val in channel_ids.items():
        print(key)
        ydg.reset_dataframe()
        ydg.get_all_videos(val, q='Trailer')
        ydg.df.to_csv(f'{key}.csv')

    df_hbo = pd.read_csv('Hbo.csv')
    df_amazon = pd.read_csv('amazon.csv')
    df_disney = pd.read_csv('disney.csv')
    df_netflix = pd.read_csv('netflix.csv')

    df_all = pd.concat((df_hbo, df_netflix, df_disney, df_amazon))
    ycg = YoutubeCommentGetter(key_gen)

    for i, video_id in enumerate(df_all.videoId):
        print(i, video_id)
        ycg.get_comments(video_id, max_requests=10)

    ycg.df.to_csv('comments.csv')