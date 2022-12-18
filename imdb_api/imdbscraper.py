import requests
import re
from bs4 import BeautifulSoup
from time import sleep
import numpy as np


class ImdbScraper:
    def __init__(self):
        self.data = {'id': [], 'release_date_us': []}

    def scrape_dates(self, tconsts, timeout=.1, verbose=False):
        for tconst in tconsts:
            response = requests.get(f'https://www.imdb.com/title/{tconst}/releaseinfo')
            soup = BeautifulSoup(response.text)
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
        for tconst in tconsts:
            if verbose:
                print(tconst)
            response = requests.get(f'https://www.imdb.com/title/{tconst}/releaseinfo')
            soup = BeautifulSoup(response.text)
            dates = re.findall('\d{1,2} [A-z]+ \d{4}', str(soup))
            dates, counts = np.unique(dates, return_counts=True)
            idx = np.argsort(-counts)
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
