# utilities.py
# By Andreas Belsager, Mads Høgenhaug, Marcus Friis & Mia Pugholm
import configparser
from time import sleep
import googleapiclient.discovery


def setup_youtube_api(DEVELOPER_KEY):
    # API information
    api_service_name = "youtube"
    api_version = "v3"

    # API client
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)
    return youtube


def timeout(func):
    def wrapper(*args, **kwargs):
        out = func(*args, **kwargs)
        sleep(.1)
        return out
    return wrapper


def get_youtube_api_key(filename):
    config = configparser.ConfigParser()
    config.read(filename)
    section = config['DEFAULT']
    for key_string in list(section):
        key = section[key_string]
        yield key
