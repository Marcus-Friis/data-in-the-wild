import requests
import re
from bs4 import BeautifulSoup
from time import sleep
import numpy as np


class ImdbScraper:
    """
    A class for scraping movie release dates from IMDb
    """

    def __init__(self):
        """
        Initialize the data attribute to store the tconst and release_date_us values
        """
        self.data = {'id': [], 'release_date_us': []}

    def scrape_dates(self, tconsts, timeout=.1, verbose=False):
        """
        Scrape the release dates for the given tconsts (IMDb movie ID).
        This method gets the first american date.
        :param tconsts: A list of IMDb movie IDs (tconsts) to scrape release dates for
        :param timeout: The time to sleep between requests. Defaults to 0.1.
        :param verbose: If set to True, prints the tconst and release date for each movie. Defaults to False.
        :return:
        """
        for tconst in tconsts:
            # get html response and parse it with BeautifulSoup
            response = requests.get(f'https://www.imdb.com/title/{tconst}/releaseinfo')
            soup = BeautifulSoup(response.text)

            # loop through all tr and find the one corresponding to US, add it to the data and break
            trs = soup.find_all('tr')
            if verbose:
                print(tconst)
            for tr in trs:
                if 'USA' in str(tr):
                    dates = re.findall('\d{1,2} [A-z]+ \d{4}', str(tr))
                    if dates:
                        if verbose:
                            print(dates)
                        self.data['id'].append(tconst)
                        self.data['release_date_us'].append(dates[0])
                        break
            sleep(timeout)

    def scrape_dates_alternate(self, tconsts, timeout=.1, verbose=False):
        """
        Scrape the release dates for the given tconsts (IMDb movie ID).
        This method gets the most frequent date on the IMDb website.
        :param tconsts: A list of IMDb movie IDs (tconsts) to scrape release dates for
        :param timeout: The time to sleep between requests. Defaults to 0.1.
        :param verbose: If set to True, prints the tconst and release date for each movie. Defaults to False.
        :return:
        """
        for tconst in tconsts:
            if verbose:
                print(tconst)

            # get html response and parse it with BeautifulSoup
            response = requests.get(f'https://www.imdb.com/title/{tconst}/releaseinfo')
            soup = BeautifulSoup(response.text)

            # find all dates and sort them in descending order
            dates = re.findall('\d{1,2} [A-z]+ \d{4}', str(soup))
            dates, counts = np.unique(dates, return_counts=True)
            idx = np.argsort(-counts)
            # if there are any dates, pick the most common one
            # if they are all equally frequent, pick the earliest date
            if dates.size > 0:
                if counts.max() > 1:
                    release_date = dates[idx][0]
                else:
                    release_date = min(dates)
                self.data['id'].append(tconst)
                self.data['release_date_us'].append(release_date)

                if verbose:
                    print(release_date)

            sleep(timeout)


if __name__ == '__main__':
    import pandas as pd
    df = pd.read_csv('../imdb/title.basics.tsv', delimiter='\t')
    scraper = ImdbScraper()
    scraper.scrape_dates_alternate(df.tconst.iloc[-10:], verbose=True)
    print(pd.DataFrame(scraper.data))

