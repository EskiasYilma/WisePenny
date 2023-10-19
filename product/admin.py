from django.contrib import admin
from .models import Category, PriceSource, SearchQuery, PriceHistory, Product, Visitors, Subscribers


# Register your models here.
admin.site.register(Category)
admin.site.register(PriceSource)
admin.site.register(SearchQuery)
admin.site.register(PriceHistory)
admin.site.register(Product)
admin.site.register(Visitors)
admin.site.register(Subscribers)
