import requests
import re
from bs4 import BeautifulSoup
from time import sleep


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


if __name__ == '__main__':
    import pandas as pd
    df = pd.read_csv('../imdb/title.basics.tsv', delimiter='\t')
    scraper = ImdbScraper()
    scraper.scrape_dates(df.tconst.iloc[-200:], verbose=True)
    print(pd.DataFrame(scraper.data))
