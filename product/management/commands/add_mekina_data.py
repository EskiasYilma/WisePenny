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

def filter_invalid_prices(products_dict):
    filtered_dict = {}
    for i, j in products_dict.items():
        try:
            price = int(j['price'])
            filtered_dict[i] = j
        except Exception as e:
            print(colored(str(e), "red"))
            pass
    return filtered_dict

class Command(BaseCommand):
    help = 'Adds scraped products to the database'

    def handle(self, *args, **options):
        # print(Product.objects.get(pk=1))
        # Define the path to your JSON file
        # json_file_path = '../../../spyders/[ALL] - Listings.json'
        json_file_path = os.path.abspath('./spyders/mekina/mekina.json')
        with open(json_file_path, 'r') as json_file:
            scraped_data = json.load(json_file)
        print(len(scraped_data))
        product_attributes = {}
        filtered_dict = filter_invalid_prices(scraped_data)
        print(len(filtered_dict))
        # for category_name, products in data.items():
        #     # Check if the category exists, or create a new one
        #     category, created = Category.objects.get_or_create(name=category_name)
        with transaction.atomic():
            for i, j in filtered_dict.items():
                print(i)
                # for k,v in j.items():
                id = int(j['id'])
                name = j['title']
                location = j['location']
                product_url = j['url']
                date_added = timezone.datetime.fromisoformat(j['date_added'])
                date_scraped = timezone.datetime.fromisoformat(j['date_scraped'])
                cat = "Vehicles"
                attributes = j['attribs']
                thumbnail_url = j['images']
                price_value = j['price']
                source_site = j['source']
                source_phone = j['phone']
                user_id = j['user_id']

                category, created = Category.objects.get_or_create(name=cat)

                price_source, created = PriceSource.objects.get_or_create(
                    # site_name=k[4],
                    # site_url=k[4],
                    source_site=source_site,
                    source_phone=source_phone,
                )
                # price_sources[j] = price_source
                # price_sources.append(price_source)
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
                    # Edit this part (if id exists and prices differ)
                    price_histories, created = PriceHistory.objects.get_or_create(
                            id=id,
                            product=Product.objects.get(id=id),
                            price=price_value,

                        )
                # Create a PriceHistory record for the product's price
                # PriceHistory.objects.create(product=products, price=price_value)
