from django.core.management.base import BaseCommand
from pennywize.models import Product, B2C
from django.db.models import Count

class Command(BaseCommand):
    help = 'Update the B2C model after loading products'

    def handle(self, *args, **kwargs):
        # Query the products to determine B2C status
        product_counts_by_phone = (
            Product.objects.values('price_source__source_phone')
            .annotate(total_products=Count('id'))
        ).filter(total_products__gt=20)

        # Update the B2C model based on the query results
        for item in product_counts_by_phone:
            source_phone = item['price_source__source_phone']
            b2c, created = B2C.objects.get_or_create(source__source_phone=source_phone)
            b2c.is_b2c = True
            b2c.save()

        self.stdout.write(self.style.SUCCESS('B2C model updated successfully'))
