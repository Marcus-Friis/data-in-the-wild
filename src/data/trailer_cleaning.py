import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def main():
    # load trailer files
    hbo = pd.read_csv('../../data/raw/trailers/hbo_trailers.csv')
    netflix = pd.read_csv('../../data/raw/trailers/netflix_trailers.csv')
    disney = pd.read_csv('../../data/raw/trailers/disney_trailers.csv')
    amazon = pd.read_csv('../../data/raw/trailers/amazon_trailers.csv')

    # for each trailer file
    for name, df in zip(['hbo', 'netflix', 'disney', 'amazon'], [hbo, netflix, disney, amazon]):
        # format title for easier comparisons
        df['title_lowered'] = df.videoTitle.str.lower()

        # create various checks that ensures the video is a trailer
        df['is_trailer'] = df.title_lowered.str.contains('trailer')
        trailer_mask = df.is_trailer == True
        official_mask = df.title_lowered.str.contains('official')
        season_mask = ~df.title_lowered.str.contains('season\s([2-9]|\d{2})')
        teaser_mask = ~df.title_lowered.str.contains('teaser')
        numbered_trailer_mask = ~df.title_lowered.str.contains('trailer.*[2-9]')

        # combine all conditions and output a new cleaned file
        mask = trailer_mask & official_mask & season_mask & teaser_mask & numbered_trailer_mask
        df[mask][list(df)[1:]].drop_duplicates().to_csv(f'../../data/interim/trailers/{name}_trailers.csv', index=False)


if __name__ == '__main__':
    main()
