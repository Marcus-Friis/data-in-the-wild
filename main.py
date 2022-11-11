# main.py
# By Andreas Belsager, Mads Høgenhaug, Marcus Friis & Mia Pugholm
import requests
import re

from youtube_api.utilities import get_youtube_api_key, setup_youtube_api
from youtube_api.youtubevideogetter import YoutubeVideoGetter


def get_scores(id):
    r = requests.get(f"https://returnyoutubedislikeapi.com/votes?videoId={id}")
    txt = r.text

    likes = int(re.findall('(?<="likes":).[0-9]+', txt)[0])
    dislikes = int(re.findall('(?<="dislikes":).[0-9]+', txt)[0])
    views = int(re.findall('(?<="viewCount":).[0-9]+', txt)[0])
    return views, likes, dislikes


if __name__ == '__main__':
    key_gen = get_youtube_api_key('config.ini')
    ydg = YoutubeVideoGetter(key_gen)
    ydg.get_all_videos('UC9InaN7Xbh39_tUSCfi-7lQ', q='')
    print(ydg.df.to_csv())
