import sys
sys.path.append('..')

from imdb_api.imdbscraper import ImdbScraper


def main():
    # get imdb entries to scrape
    import pandas as pd
    match = pd.read_csv('../../data/interim/match.csv')

    # instantiate object and start scraping
    scraper = ImdbScraper()
    scraper.scrape_dates_alternate(match.tconst, verbose=True, timeout=1)

    # format new release dates dataframe
    release_dates = pd.DataFrame(scraper.data)
    release_dates['releaseDateUS'] = pd.to_datetime(release_dates.release_date_us)

    # output scraped data
    release_dates.to_csv('../../data/interim/release_dates.csv', index=False)


if __name__ == '__main__':
    main()
