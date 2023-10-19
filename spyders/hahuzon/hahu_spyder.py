import requests
from bs4 import BeautifulSoup as soup
from termcolor import colored
from datetime import datetime
from pytz import timezone
import json
import time

def format_datetime(str_date):
    input_date = "August 25, 2023 10:35 am"
    parsed_date = datetime.strptime(input_date, "%B %d, %Y %I:%M %p")
    formatted_date = parsed_date.strftime("%Y-%m-%dT%H:%M:%S.%f%z")
    return(formatted_date)

class Hahu_spyder:
    def __init__(self):
        self.headers = {
            'authority': 'hahuzon.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'referer': 'https://hahuzon.com/',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        }
        self.url = "https://hahuzon.com/listing-category/electronics/"
        self.s = requests.Session()
        self.usp = self.r_n_s(self.url)
        self.total_pages = int(self.usp.find('div', {'class':'pagination-area'}).ul.find_all('li')[-2].a.text.strip())
        # print(self.total_pages)
        self.links = {}
        self.data = {}
        self.total_listings = 0

    def r_n_s(self, url):
        """
        request_n_get_soup
        """
        r = self.s.get(url, headers=self.headers)
        return soup(r.content, 'lxml')

    def get_links(self):
        for i in range(1, self.total_pages):
            time.sleep(1)
            print(colored("On Page [{}] - [{}]...".format(i, self.total_pages), "yellow"))
            url = self.url + "page/{}/".format(i) + "?orderby=date-asc"
            usp = self.r_n_s(url)
            link_cont = usp.find_all('h3', {'class':'listing-title'})
            for i, links in enumerate(link_cont):
                self.total_listings += 1
                link = links.a['href']
                print(colored(link, "cyan"))
                try:
                    self.get_details(link)
                except Exception as e:
                    print(colored(str(e), "red"))
                    pass
                print(colored("{} listings added.".format(self.total_listings), "green"))
                time.sleep(0.7)

    def get_details(self, link):
        """
        category
        source_site
        source_phone
        id
        name
        location
        product_url
        date_added
        date_scraped
        attributes
        thumbnail_url
        price_value
        """
        usp = self.r_n_s(link)
        id = usp.find('div', {'class':'rtin-chat'}).a['data-listing_id']
        name = usp.find('h1', {'class':'entry-title'}).text.strip()
        try:
            location = usp.find('div', {'class':'rtin-location'}).div.find_all('div')[-1].text.strip()
        except Exception:
            try:
                location = usp.find('div', {'class':'rtin-location'}).div.find_all('div')[0].text.strip()
            except Exception:
                location = "N/A"
                pass
        product_url = link
        date_added = format_datetime(usp.find('ul', {'class':'single-listing-meta'}).find_all('li')[0].text.strip())
        date_scraped = datetime.now(timezone('UTC')).isoformat()
        attributes = "\n".join([x.text.strip() for x in usp.find('div',{'class':'rtin-content'}).find_all('p')])
        thumb_url = usp.find('meta',{'property':'og:image'})['content']
        price_value = usp.find('span', {'class':'amount'}).text.strip().replace(" ", "").replace("Br", "").replace(",", "")
        category =  usp.find('ul', {'class':'trail-items'}).find_all('li')[-2].a.span.text.strip()
        source_site = "Hahuzon.com"
        source_phone = usp.find('div', {'class':'numbers'}).text.strip()
        self.data[id] = {'id':id, 'name':name, 'location':location, 'product_url':product_url, 'date_added':date_added, 'date_scraped':date_scraped, 'attributes':attributes, 'thumb_url':thumb_url, 'price_value':price_value, 'category':category, 'source_site':source_site, 'source_phone':source_phone}


hahu = Hahu_spyder()
try:
    hahu.get_links()
except Exception as e:
    print(colored(str(e), "red"))
with open("/home/ex/Documents/GITLAB/ghost_modules/ghost_prices/test/mini_price/spyders/hahuzon/hahuzon.json", 'w') as f:
    json.dump(hahu.data, f)
