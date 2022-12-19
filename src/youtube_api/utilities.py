import configparser
from time import sleep
import googleapiclient.discovery


# set up the YouTube API using the given developer key
def setup_youtube_api(DEVELOPER_KEY):
    # API information
    api_service_name = "youtube"
    api_version = "v3"

    # API client
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)
    return youtube


# a decorator function to add a timeout of 0.1 seconds before calling the decorated function
def timeout(func):
    def wrapper(*args, **kwargs):
        # call the decorated function and store the output
        out = func(*args, **kwargs)
        # sleep for 0.1 seconds
        sleep(.1)
        # return the output of the decorated function
        return out
    # return the wrapper function
    return wrapper


# get the YouTube API keys from the given filename
def get_youtube_api_key(filename):
    # read the config file
    config = configparser.ConfigParser()
    config.read(filename)
    # get the default section of the config file
    section = config['DEFAULT']
    # iterate over the keys in the default section
    for key_string in list(section):
        # get the key
        key = section[key_string]
        # iield the key
        yield key
