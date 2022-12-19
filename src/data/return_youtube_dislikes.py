import requests
import re
import pandas as pd
import time
import numpy as np


# Function to call the returnyoutubedislike api. 
# This api is simply a website, where you plug in the video ID as seen in the 2nd line of the block. 
# It returns a json object, where we can get various information about the given video, such as likes, dislikes, and viewcount. 

def load_data():
    df = pd.read_csv('../../data/interim/trailers.csv')
    df = list(df.videoId)
    return df


def get_scores(id):
    r = requests.get(f"https://returnyoutubedislikeapi.com/votes?videoId={id}")
    vals = r.json()
    likes, dislikes, viewCount = vals["likes"], vals["dislikes"],vals["viewCount"]
    return likes,dislikes, viewCount


# Loops through all the video IDs (which are listed below this cell), and:
# 1) Checks if the video is already in the dataframe.
# 2) Checks if it's the first iteration. If thats true, then it creates a dataframe with the likes, dislikes, and viewcount.
# 3) Continues to call the get_scores() functions on the ids, and updates the dataframe

#loop through all video IDS
def create_df(list_of_ids):
    for num,i in enumerate(range(len(list_of_ids))):
        #checks if video is in dataframe already (if it's created)
        try:
            if list_of_ids[i] == df.videoId[i]:
                print(num,"id already exists,continueing")
        except (NameError,KeyError):
            #If video not in the dataframe, then the get_scores() function is called to acquire the video's metrics that we want. 
            print(num,list_of_ids[i])
            likes,dislikes, viewCount = get_scores(list_of_ids[i])
            #If it's the first iteration (and the ID is not in the dataframe), a dataframe is then constructed.
            if i == 0:
                print("creating df")
                d = {"videoId": list_of_ids[i], "likes": likes,"dislikes": dislikes,"viewCount": viewCount}
                df = pd.DataFrame(data=d, index=[0])
            #After the first iteration: A temporary dataframe is constructed, and then appended to the original dataframe.
            else:
                temp_df = pd.DataFrame({"videoId": list_of_ids[i], "likes": likes,"dislikes": dislikes,"viewCount": viewCount},index=[i])
                df = df.append(temp_df,ignore_index = True)
            #1 second wait time between each iteration, to avoid getting locked out from the API. 
            time.sleep(1)
    return df


def main():
    #load data and get list of ids
    ids = load_data()
    #parse list of ids to function, and get likes, dislikes, viewCount
    df = create_df(ids)
    #save new csv
    df.to_csv("../../data/raw/returnyoutubedislikes.csv",index = False)



if __name__ == '__main__':
    main()
