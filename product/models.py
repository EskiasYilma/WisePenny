from django.contrib.auth.models import User
from django.db import models
import hashlib
import jsonfield
from django.db.models import Q, Count

class Category(models.Model):
    """
    Category of the product
    """
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class SearchQuery(models.Model):
    """
    Stores Search Terms from all users (registered and anonymouse)
    """
    search_term = models.CharField(max_length=255)
    date_searched = models.DateTimeField(auto_now_add=True)
    counter = models.IntegerField(default=0)

class PriceHistory(models.Model):
    """
    Stores Price History of the product
    """
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

class PriceSource(models.Model):
    """
    Stores Price Source of the product
    """
    source_phone = models.CharField(max_length=255)
    source_site = models.CharField(max_length=255)
    product_count = models.IntegerField(default=0)
    is_b2c = models.BooleanField(default=False)

    class Meta:
        unique_together = ['source_phone', 'source_site']

    def __str__(self):
        return "{} - {}".format(self.source_phone, self.product_count)

    def save(self, *args, **kwargs):
        if self.product_count > 30:
            self.is_b2c = True
        else:
            self.is_b2c = False
        super(PriceSource, self).save(*args, **kwargs)

class Product(models.Model):
    """
    Stores the product
    """
    id = models.AutoField(primary_key=True, unique=True,)
    name = models.CharField(max_length=255)
    location = models.TextField(blank=True, null=True)
    product_url = models.URLField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # JSONField to store flexible attributes
    attributes = jsonfield.JSONField(blank=True, null=True)
    price_value = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    price_source = models.ForeignKey(PriceSource, on_delete=models.CASCADE)
    thumbnail_url = models.URLField(null=True, blank=True)
    date_added = models.DateTimeField()
    date_scraped = models.DateTimeField()
    fingerprint = models.CharField(max_length=32, unique=True, editable=False)
    # Save images optional
    # thumbnail = models.ImageField(upload_to='images/user/img/', null=True, blank=True)
    class Meta:
        unique_together = ['id', 'name', 'product_url', 'category', 'price_value', 'price_source', 'thumbnail_url']
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Check if the product is being created (not yet saved to the database)
        is_new_product = self._state.adding
        # Calculate the fingerprint using MD5 hash of key attributes
        fingerprint_data = f"{self.id}{self.name}{self.product_url}{self.category}{self.price_value}{self.price_source}{self.thumbnail_url}"
        self.fingerprint = hashlib.md5(fingerprint_data.encode('utf-8')).hexdigest()
        super(Product, self).save(*args, **kwargs)

        # Update the product_count for the related PriceSource
        price_source = self.price_source
        price_source.product_count = price_source.product_set.count()
        price_source.save()


class Visitors(models.Model):
    """
    Stores Website Visitors
    """
    visitor_ip = models.TextField(max_length=20, unique=True)
    visit_count = models.IntegerField(default=0)


class ProductTracker(models.Model):
    """
    Stores Products set to be tracked by a registerd user
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_products", null=True)
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    date_added = models.DateTimeField(auto_now_add=True)
    tracked = models.BooleanField(default=False)
    search_results = models.ManyToManyField(Product, related_name="tracked_by", blank=True)

    class Meta:
        unique_together = ['user', 'name']

    def __str__(self):
        return self.name

    def get_related_products(self):
        return Product.objects.select_related('category', 'price_source').filter(Q(name__icontains=self.name)).order_by("price_value")

    def get_last_update(self):
        try:
            return Product.objects.select_related('category', 'price_source').filter(Q(name__icontains=self.name)).order_by("date_scraped")[0]
        except Exception:
            return None

class Subscribers(models.Model):
    """
    Stores Subscribers
    """
    sub_email = models.EmailField(unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sub_email}"
