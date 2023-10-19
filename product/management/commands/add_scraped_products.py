import json
from django.core.management.base import BaseCommand
from django.utils import timezone
from pennywize.models import Category, Product, PriceSource, SearchQuery
import os
import requests
from django.core.files import File
import time

def download_image(id, image_url, product_instance):
    time.sleep(0.7)
    file_name = "{}.{}".format(id, image_url.split(".")[-1])
    image_path = "/home/ex/Documents/GITLAB/ghost_modules/ghost_prices/test/wisepenny/spyders/images/{}".format(file_name)
    try:
        r = requests.get(image_url, allow_redirects=True)#(image_url, allow_redirects=True)
        if r.status_code == 200:
            # Create a file name for the image (you can customize this as needed)

            open(image_path, 'wb').write(r.content)
            # Save the image content to the 'thumbnail' field
            print("{} - Image saved".format(id))

            return image_path
            # product_instance.thumbnail.save(file_name, File(open(r[0], 'rb')))
        else:
            print("Failed to download image")
            return None
    except Exception as e:
        print(str(e))
        return None

def filter_invalid_prices(price_dict):
    filtered_dict = {key: value for key, value in price_dict.items() if value[0] is not None}
    return filtered_dict

class Command(BaseCommand):
    help = 'Adds scraped products to the database'

    def handle(self, *args, **options):
        # Define the path to your JSON file
        # json_file_path = '../../../spyders/[ALL] - Listings.json'
        json_file_path = os.path.abspath('./spyders/[ALL] - Listings.json')
        with open(json_file_path, 'r') as json_file:
            scraped_data = json.load(json_file)
        print(len(scraped_data))
        product_attributes = {}
        # for category_name, products in data.items():
        #     # Check if the category exists, or create a new one
        #     category, created = Category.objects.get_or_create(name=category_name)
        for i, j in scraped_data.items():
            # print(i, len(j))
            for products in j:
                attributes_dict = {}
                for product_id, product_data in products.items():
                    price = product_data[4]['price']
                    name = product_data[1]['title']
                    id = product_id
                    product_url = product_data[12]['url']
                    source_name = product_data[13]['source']
                    description = "{} - {}".format(product_data[5]['city'], product_data[6]['sub_city'])
                    category = product_data[2]['main_cat']
                    attrib_data = product_data[7]['attrs']
                    for data_dict in attrib_data:
                        for key, value in data_dict.items():
                            attributes_dict[key] = value
                    date_added = product_data[-2]['date_added']
                    date_scraped = product_data[-1]['date_scraped']
                    user_id = product_data[-7]['user_id']
                    thumbnail_url = product_data[-5]['images']
                    phone = product_data[-8]['phone']

                    product_attributes[id] = [price, name, id, product_url, source_name, description, category, attributes_dict, date_added, date_scraped, user_id, thumbnail_url, phone]

                    # print(product_id, product_data[4]['price'])
        # Filter None
        filtered_product_attributes = filter_invalid_prices(product_attributes)
        prices = list()
        price_sources = {}
        new_price = list()
        price_change = list()

        price_types = []
        for i, (j, k) in enumerate(filtered_product_attributes.items()):
            print(i, j)

            # prices.append(j[0])
            # price_types.append(type(j[0]))
            # print(set(price_types))
            category, created = Category.objects.get_or_create(name=k[6])

            price_source, created = PriceSource.objects.get_or_create(
                site_name=k[4],
                site_url=k[4],
                source_name=k[-3],
                source_phone=k[-1],
            )
            # price_sources[j] = price_source
            # price_sources.append(price_source)
            products, created = Product.objects.get_or_create(name= k[1],
                    location= k[5],
                    product_url= k[3],
                    date_added= timezone.datetime.fromisoformat(k[-5]),
                    date_scraped=timezone.datetime.fromisoformat(k[-4]),
                    category= category,
                    attributes= k[7],
                    thumbnail_url= k[-2],
                    price_value=k[0],
                    price_source=price_source)
            price_source.save()
            products.save()
            # Create or update the Product model
            # image_url = k[-2]
            # # thumbnail = download_image(image_url)
            # product, created = Product.objects.update_or_create(
            #     id=int(j),
            #     defaults={
            #         'name': k[1],
            #         'description': k[5],
            #         'product_url': k[3],
            #         'date_added': timezone.datetime.fromisoformat(k[-5]),
            #         'category': category,
            #         'attributes': k[7],
            #         'thumbnail_url': k[-2]
            #         # Add other fields as needed
            #     }
            # )
            # thumb = download_image(i, image_url, product)
            # product.thumbnail = thumb
            # product.save()
            # price_sources.append(PriceSource(site_name=k[4],
            #     site_url=k[4],
            #     source_name=k[-3],
            #     source_phone=k[-1]))
            # # Create or update the PriceSource model
            # # price_source, created = PriceSource.objects.get_or_create(
            # #     site_name=k[4],
            # #     site_url=k[4],
            # #     source_name=k[-3],
            # #     source_phone=k[-1],
            # # )
            # # Check if there's an existing price for this product
            # existing_price = Price.objects.filter(product=product).order_by('-date_scraped').first()

            # # Create a new Price record
            # new_price.append(
            #     product=product,
            #     price_value=k[0],
            #     date_scraped=timezone.datetime.fromisoformat(k[-4]),
            #     source=price_source
            #     )
            # # new_price = Price(
            # #     product=product,
            # #     price_value=k[0],
            # #     date_scraped=timezone.datetime.fromisoformat(k[-4]),
            # #     source=price_source,
            # # )
            # # new_price.save()
            # # Check if the price has changed
            # if existing_price and existing_price.price_value != new_price.price_value:
            #     # Create a PriceChange record to track the change
            #     price_change.append(PriceChange(
            #         product=product,
            #         price_value=new_price.price_value,
            #         date_changed=new_price.date_scraped
            #         ))
                # price_change = PriceChange(
                #     product=product,
                #     price_value=new_price.price_value,
                #     date_changed=new_price.date_scraped,
                # )
                # price_change.save()
        # PriceSource.objects.bulk_create(price_sources.values(), ignore_conflicts=True)
        # Product.objects.bulk_create(prices, ignore_conflicts=True)
