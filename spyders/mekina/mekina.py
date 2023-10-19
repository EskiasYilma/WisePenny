import requests
from bs4 import BeautifulSoup as soup
import time
from datetime import datetime
from pytz import timezone
import json
from termcolor import colored


class Mekina:
    def __init__(self):
        self.headers = {
            'authority': 'www.mekina.net',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        }

        self.params = {}
        self.category = "Vehicles"
        self.listing_dict = {}
        self.s = requests.Session()
        self.listing_data = {}
        self.total_listings = 0

    def get_total_pages(self):
        self.params['s'] = ''
        response = self.s.get('https://www.mekina.net/', params=self.params, headers=self.headers)
        usp = soup(response.text, 'lxml')
        pages = int(usp.find('ul', {'class':'pagination'}).find_all('li')[-2].text.strip())
        # TODO: Checkers - 12 listings per page
        print(pages)
        for i in range(1, pages+1):
            print(colored("on Page [{}] of [{}]".format(i, pages), "yellow"))
            time.sleep(1)
            self.get_listing_links(i)

    def get_listing_links(self, page):
        r = self.s.get('https://www.mekina.net/page/{}'.format(page))
        usp = soup(r.text, 'lxml')
        links = usp.find_all('h3', {'itemprop':'name'})
        for i,j in enumerate(links):
            time.sleep(1)
            link = j.a['href']
            print(link)
            try:
                self.get_details(link)
            except Exception as e:
                print(colored(str(e), "red"))
                pass

    def get_details(self, link):
        r = self.s.get(link)
        usp = soup(r.text, 'lxml')
        id = usp.find('link', {'rel':'shortlink'})['href'].split("=")[-1]
        title = usp.find('h1', {'itemprop':'name'}).text.strip()
        price = usp.find('div', {'class':'singleprice-tag'}).text.strip().replace("ብር ", "").replace(",", "")
        if "(" in str(price):
            price = price.split("(")[0]
        condition = usp.find('strong', text="Condition").parent.parent.text.strip().split(":")[1].strip()
        date_added = usp.find('meta', {'property':'og:updated_time'})['content']
        date_scraped = datetime.now(timezone('UTC')).isoformat()
        phone = usp.find('a', {'class':'number'})['data-last'].replace(" ", "").strip()
        user_id = usp.find('meta', {'property':'article:author'})['content'].split("/")[-2]
        images = usp.find('meta', {'itemprop':'image'})['content']
        url = link
        source = "Mekina.net"
        location = usp.find('strong', text="Location").parent.parent.text.strip().split(":")[1].strip()
        attrs = usp.find('div', {'class':'short-features'}).find_all('div', {'class':'details'})
        a = {}
        for i in attrs:
            text = i.text.strip().split(":")
            a[text[0]] = text[1]
        print(id)
        # title =
        self.listing_data[id] = {'id':id, 'title':title, 'price':price, 'condition':condition, 'date_added':date_added, 'date_scraped':date_scraped, 'phone':phone, 'user_id':user_id, 'images':images, 'url':url, 'source':source, 'location':location, 'attribs':a}
        self.total_listings += 1
        print(colored("[{}] - listings added.".format(self.total_listings), "green"))

mekina = Mekina()
mekina.get_total_pages()
with open("/home/ex/Documents/GITLAB/ghost_modules/ghost_prices/test/mini_price/spyders/mekina/mekina.json", 'w') as f:
    json.dump(mekina.listing_data, f)
