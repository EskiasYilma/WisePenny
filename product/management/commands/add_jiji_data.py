import json
from django.core.management.base import BaseCommand
from django.utils import timezone
from product.models import Category, Product, PriceSource, SearchQuery, PriceHistory
import os
import requests
from django.core.files import File
import time
from django.db import transaction


def filter_invalid_prices(price_dict):
    """
    Filters Invalid Prices
    """
    filtered_dict = {key: value for key, value in price_dict.items() if value[0] is not None}
    return filtered_dict

class Command(BaseCommand):
    help = 'Adds scraped products to the database'

    def handle(self, *args, **options):
        json_file_path = os.path.abspath('./spyders/[ALL] - Listings.json')
        with open(json_file_path, 'r') as json_file:
            scraped_data = json.load(json_file)
        print(len(scraped_data))
        product_attributes = {}

        for i, j in scraped_data.items():
            for products in j:
                attributes_dict = {}
                for product_id, product_data in products.items():
                    price = product_data[4]['price']
                    name = product_data[1]['title']
                    id = product_id
                    product_url = product_data[12]['url']
                    source_name = product_data[13]['source']
                    description = "{} - {}".format(product_data[5]['city'], product_data[6]['sub_city'])
                    category = product_data[3]['cat_name']
                    main_cat = product_data[2]['main_cat']
                    attrib_data = product_data[7]['attrs']
                    for data_dict in attrib_data:
                        for key, value in data_dict.items():
                            attributes_dict[key] = value
                    date_added = product_data[-2]['date_added']
                    date_scraped = product_data[-1]['date_scraped']
                    user_id = product_data[-7]['user_id']
                    thumbnail_url = product_data[-5]['images']
                    phone = product_data[-8]['phone']

                    product_attributes[id] = [price, name, id, product_url, source_name, description, category, attributes_dict, date_added, date_scraped, user_id, thumbnail_url, phone, main_cat]

        filtered_product_attributes = filter_invalid_prices(product_attributes)
        prices = list()
        price_sources = {}
        new_price = list()
        price_change = list()

        price_types = []
        with transaction.atomic():
            for i, (j, k) in enumerate(filtered_product_attributes.items()):
                print(i, j)

                if k[-1] == "Electronics":

                    category, created = Category.objects.get_or_create(name=k[6])

                    price_source, created = PriceSource.objects.get_or_create(
                        source_site=k[4],
                        source_phone=k[-2],
                    )

                    try:
                        products, created = Product.objects.get_or_create(
                            id=k[2],
                            name= k[1],
                                location= k[5],
                                product_url= k[3],
                                date_added= timezone.datetime.fromisoformat(k[-6]),
                                date_scraped=timezone.datetime.fromisoformat(k[-5]),
                                category= category,
                                attributes= k[7],
                                thumbnail_url= k[-3],
                                price_value=k[0],
                                price_source=price_source)
                    except Exception as e:
                        print("In exception - {}".format(e))
                        price_histories, created = PriceHistory.objects.get_or_create(
                                id=k[2],
                                product=Product.objects.get(id=k[2]),
                                price=k[0],
    
                            )                        
