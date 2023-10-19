import json
from django.core.management.base import BaseCommand
from django.utils import timezone
from product.models import Category, Product, PriceSource, SearchQuery, PriceHistory
import os
import requests
from django.core.files import File
import time
from termcolor import colored
from django.db import transaction
from ast import literal_eval

def filter_invalid_prices(products_dict):
    """
    Filters Invalid Prices
    """    
    filtered_dict = {}
    for i, j in products_dict.items():
        try:
            price = int(j['price_value'])
            filtered_dict[i] = j
        except Exception as e:
            print(colored(str(e), "red"))
            pass
    return filtered_dict

class Command(BaseCommand):
    help = 'Adds scraped products to the database'

    def handle(self, *args, **options):
        json_file_path = os.path.abspath('./spyders/hahuzon/hahuzon.json')
        with open(json_file_path, 'r') as json_file:
            scraped_data = json.load(json_file)
        product_attributes = {}
        filtered_dict = filter_invalid_prices(scraped_data)
        with transaction.atomic():
            for i, j in filtered_dict.items():
                print(i)
                id = int(j['id'])
                name = j['name']
                location = j['location']
                product_url = j['product_url']
                date_added = timezone.datetime.fromisoformat(j['date_added'])
                date_scraped = timezone.datetime.fromisoformat(j['date_scraped'])
                cat = j['category']
                attributes = {"attrs":" -||- ".join(j['attributes'].split("\n"))}
                thumbnail_url = j['thumb_url']
                price_value = j['price_value']
                source_site = j['source_site']
                source_phone = j['source_phone']
                category, created = Category.objects.get_or_create(name=cat)

                price_source, created = PriceSource.objects.get_or_create(
                    source_site=source_site,
                    source_phone=source_phone,
                )
                try:
                    products, created = Product.objects.get_or_create(
                            id=id,
                            name=name,
                            location=location,
                            product_url=product_url,
                            date_added=date_added,
                            date_scraped=date_scraped,
                            category=category,
                            attributes=attributes,
                            thumbnail_url=thumbnail_url,
                            price_value=price_value,
                            price_source=price_source)
                except Exception:
                    print(colored("in Exception", "red"))
                    price_histories, created = PriceHistory.objects.get_or_create(
                            id=id,
                            product=Product.objects.get(id=id),
                            price=price_value,

                        )
