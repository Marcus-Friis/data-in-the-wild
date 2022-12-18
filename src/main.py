# main.py
# By Andreas Belsager, Mads Høgenhaug, Marcus Friis & Mia Pugholm
import pandas as pd
import requests
import re

from youtube_api.utilities import get_youtube_api_key, setup_youtube_api
from youtube_api.youtubevideogetter import YoutubeVideoGetter
from youtube_api.youtubecommentgetter import YoutubeCommentGetter


if __name__ == '__main__':

    run = input('What do you want to do?\nScrape trailers?\t(1)\nScrape comments?\t(2)\nYour input: ')
    key_gen = get_youtube_api_key('config.ini')

    if run == '1':
        channel_ids = {
            'netflix': 'UCWOA1ZGywLbqmigxE4Qlvuw',
            'hbo': 'UCx-KWLTKlB83hDI6UKECtJQ',
            'amazon': 'UCwSIJCMWZC5GDM59wj7pMsg',
            'disney': 'UCIrgJInjLS2BhlHOMDW7v0g'
        }

        ydg = YoutubeVideoGetter(key_gen)
        for key, val in channel_ids.items():
            print(key)
            ydg.reset_dataframe()
            ydg.get_videos(val, q='Trailer')
            ydg.df.to_csv(f'../data/raw/trailers/{key}_trailers.csv')

    if run == '2':
        df_hbo = pd.read_csv('../data/raw/trailers/hbo_trailers.csv')
        df_amazon = pd.read_csv('../data/raw/trailers/amazon_trailers.csv')
        df_disney = pd.read_csv('../data/raw/trailers/disney_trailers.csv')
        df_netflix = pd.read_csv('../data/raw/trailers/netflix_trailers.csv')

        df_dict = {
            'hbo': df_hbo,
            'amazon': df_amazon,
            'disney': df_disney,
            'netflix': df_netflix
        }

        ycg = YoutubeCommentGetter(key_gen)

        for name, df in df_dict.items():
            print(name)
            for i, video_id in enumerate(df.videoId):
                print(i, video_id)
                ycg.get_comments(video_id, max_requests=float('inf'))

            ycg.df.to_csv(f'../data/raw/comments/{name}_comments.csv')
            ycg.reset_dataframe()
