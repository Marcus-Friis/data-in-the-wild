import sys
sys.path.append('../../')

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import seaborn as sns

from src.sentiment import sentiment_vader
from src.imdb_api.imdbscraper import ImdbScraper

from scipy import stats

from datetime import datetime


def main():
    prompt = """Apply vader sentiment (takes a long time)?:
             yes\t(1)
             no \t(2)
             Your answer: """
    inp = input(prompt)

    # load an prepare trailers data
    file_list = ['hbo', 'amazon', 'netflix', 'disney']
    dfs = []
    for file in file_list:
        df = pd.read_csv('../../data/interim/trailers/' + file + '.csv')
        df['network'] = file
        dfs.append(df)

    cols = ['channelId', 'network', 'videoId', 'videoTitle', 'publishTime']
    trailers = pd.concat(dfs)[cols]

    # load and prepare comments data
    file_list = ['hbo_comments', 'amazon_comments', 'netflix_comments', 'disney_comments']
    dfs = []
    for file in file_list:
        df = pd.read_csv('../../data/raw/comments/' + file + '.csv')
        dfs.append(df)

    comments = pd.concat(dfs)
    cols = ['videoId', 'commentId', 'textOriginal', 'likeCount', 'publishedAt']
    comments = comments[cols]

    # load and prepare match data
    file_list = ['hbo', 'amazon', 'netflix', 'disney']
    dfs = []
    for file in file_list:
        df = pd.read_csv('../../data/interim/match/' + file + '_match.csv', delimiter=';')
        dfs.append(df)

    match = pd.concat(dfs).dropna()

    # load and prepare IMDb data
    imdb = pd.read_csv('../../data/external/imdb/title.basics.tsv', delimiter='\t')
    ratings = pd.read_csv('../../data/external/imdb/title.ratings.tsv', delimiter='\t')
    imdb = imdb.merge(ratings, on='tconst')

    # load and prepare IMDb release dates
    release_dates = pd.read_csv('../../data/interim/release_dates.csv')
    cols = ['id', 'release_date_us']
    release_dates = release_dates[cols]
    release_dates = release_dates.rename(columns={'id': 'tconst', 'release_date_us': 'releaseDateUS'})

    # load and prepare annotations
    annot = pd.read_csv('../../data/interim/annotated.csv')
    annot = annot[['commentId', 'sentiment', 'annotator']]

    annot_agg = annot.groupby('commentId').agg(
        sentimentLabel=('sentiment', stats.mode)
    ).reset_index()

    annot_agg.sentimentLabel = annot_agg.sentimentLabel.str[0].str[0]

    sentiment_map = {'Positive': 1, 'Neutral': 0, 'Negative': -1}
    annot_agg['sentimentScore'] = annot_agg.sentimentLabel.map(sentiment_map)

    # load and prepare Return YouTube Dislikes
    ryd = pd.read_csv('../../data/raw/returnyoutubedislikes.csv')
    ryd = ryd[['videoId', 'likes', 'dislikes', 'viewCount']]

    # join all dataframes together
    df = trailers.merge(comments, on='videoId')
    df = df.merge(ryd, on='videoId', how='left')
    df = df.merge(match, on='videoId')
    df = df.merge(imdb, on='tconst')
    df = df.merge(release_dates, on='tconst', how='left')
    df = df.merge(annot_agg, on='commentId', how='left')

    # add an comment date offset column
    dt = pd.to_datetime(df.publishedAt)
    comment_date = dt.dt.date
    df['releaseDateUS'] = pd.to_datetime(df.releaseDateUS)
    df['commentDateOffset'] = (pd.to_datetime(comment_date) - df.releaseDateUS)
    df['commentDateOffset'] = df.commentDateOffset.astype('timedelta64[D]').astype('float')

    # optionally, add sentiment
    if inp == '1':
        df['sentimentPredictedRaw'] = df.textOriginal.astype(str).apply(sentiment_vader)
        sentiment_map = {'Positive': 1, 'Neutral': 0, 'Negative': -1}
        df['sentimentPredictedScore'] = df.sentimentPredictedRaw.str[-1].map(sentiment_map)

    now = str(datetime.now())
    df.to_csv(f'{now}_data.csv', index=False)


if __name__ == '__main__':
    main()

