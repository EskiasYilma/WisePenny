import json
from django.core.management.base import BaseCommand
from django.utils import timezone
from pennywize.models import Category, Product, PriceSource, SearchQuery
import pandas as pd
from django.db.models import Sum, Count

class Command(BaseCommand):
    help = 'Adds scraped products to the database'

    def handle(self, *args, **options):
        # queryset = Product.objects.select_related('category', 'price_source').order_by('-date_added')
        # data = [model.__dict__ for model in queryset]
        # df = pd.DataFrame(data)
        # # group by phone number
        # print(df['name'][0])


        queryset = Product.objects.select_related('price_source', 'category')

        # Convert the queryset to a list of dictionaries
        data = [
            {
                'name': product.name,
                'location': product.location,
                'product_url': product.product_url,
                'category': product.category.name,  # Assuming you want the category name
                'attributes': product.attributes,
                'price_value': product.price_value,
                'price_source_site_name': product.price_source.site_name,  # Access PriceSource fields
                'price_source_site_url': product.price_source.site_url,
                'price_source_source_name': product.price_source.source_name,
                'price_source_source_phone': product.price_source.source_phone,
                'thumbnail_url': product.thumbnail_url,
                'date_added': product.date_added,
                'date_scraped': product.date_scraped,
                'fingerprint': product.fingerprint
            }
            for product in queryset
        ]
        df = pd.DataFrame(data)
        b2c = df.groupby(['price_source_site_name', 'price_source_source_phone'])['name'].agg('count').reset_index()
        b2c_filtered = b2c[b2c['name'] >= 20]
        print(df.columns)
        print(b2c)
        print(b2c_filtered)
        product_counts_by_phone = (
            Product.objects.values('price_source__source_phone')
            .annotate(total_products=Count('id'))
        ).filter(total_products__gt=20)
        print(product_counts_by_phone)
