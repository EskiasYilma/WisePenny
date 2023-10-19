# import pandas as pd
from product.models import Category, Product, PriceSource, SearchQuery, Visitors
from django.db.models import Sum
from django.db.models import Max, Min, Count
from django.db.models import F
from django.db.models import Q
from django.db.models.functions import Coalesce
from django.db import models
from termcolor import colored


class SearchQuery_Manager:
    """
    Saves and retrives search terms made by all users
    """
    def __init__(self, search_term=None):
        self.search_term = search_term

    def save_search(self, request):
        # Try to update an existing record
        search, created = SearchQuery.objects.get_or_create(search_term=self.search_term, defaults={'counter': 0})
        search.counter = F('counter') + 1
        search.save()

    def search_reports(self):
        recent_searches = SearchQuery.objects.values('search_term').annotate(counter=Sum('counter')).order_by('-counter')[:50]
        return recent_searches

def get_all_data():
    """
    Retrives all current database summary
    """
    main_search = Product.objects.select_related('price_source').all().order_by("price_value")
    total_categories = main_search.values('category__name').distinct().count()

    # Total number of sellers
    total_number_of_sellers = main_search.values('price_source').distinct().count()

    # Price range (min-max)
    price_range = main_search.aggregate(min_price=Min('price_value'), max_price=Max('price_value'))
    min_price = price_range['min_price']
    max_price = price_range['max_price']
    try:
        min_price = f"ETB {min_price:,.2f}"
        max_price = f"ETB {max_price:,.2f}"
    except Exception:
        pass

    # Total number of locations
    total_number_of_locations = main_search.values('location').distinct().count()

    # Total number of B2Cs and C2Cs
    total_b2cs = main_search.filter(price_source__is_b2c=True).values('price_source').distinct().count()
    total_c2cs = total_number_of_sellers - total_b2cs
    print(total_number_of_sellers)
    print(total_b2cs)
    print(colored(total_c2cs, "red"))

    # Latest post date
    latest_date_added = main_search.aggregate(latest_date=Max('date_added'))['latest_date']

    # Create the JSON result
    summary_data = {
        'sellers': total_number_of_sellers,
        'price_range': f"{min_price} - {max_price}",
        'locations': total_number_of_locations,
        'B2Cs': total_b2cs,
        'C2Cs': total_c2cs,
        'latest_post': latest_date_added.strftime('%Y-%m-%d %H:%M:%S') if latest_date_added else None,
        'products': main_search.count(),
        'total_categories':total_categories
    }

    return summary_data, main_search

def get_summary_data(search_term=""):
    """
    Retrives all database summary that relates to the search term provided by the user
    """
    main_search = None
    if search_term == "":
        main_search = Product.objects.select_related('category', 'price_source').all().order_by("price_value")
    else:
        main_search = Product.objects.select_related('category', 'price_source').filter(Q(name__icontains=search_term) | Q(category__name__icontains=search_term)).order_by("price_value")
    # Total number of sellers
    total_number_of_sellers = main_search.values('price_source').distinct().count()

    # Price range (min-max)
    price_range = main_search.aggregate(min_price=Min('price_value'), max_price=Max('price_value'))
    min_price = price_range['min_price']
    max_price = price_range['max_price']
    try:
        min_price = f"ETB {min_price:,.2f}"
        max_price = f"ETB {max_price:,.2f}"
    except Exception:
        pass

    # Total number of locations
    total_number_of_locations = main_search.values('location').distinct().count()

    # Total number of B2Cs and C2Cs
    total_b2cs = main_search.filter(price_source__is_b2c=True).count()
    total_c2cs = total_number_of_sellers - total_b2cs
    print(total_number_of_sellers)
    print(total_b2cs)
    print(colored(total_c2cs, "red"))

    # Latest post date
    latest_date_added = main_search.aggregate(latest_date=Max('date_added'))['latest_date']

    # Create the JSON result
    summary_data = {
        'sellers': total_number_of_sellers,
        'price_range': f"{min_price} - {max_price}",
        'locations': total_number_of_locations,
        'B2Cs': total_b2cs,
        'C2Cs': total_c2cs,
        'latest_post': latest_date_added.strftime('%Y-%m-%d %H:%M:%S') if latest_date_added else None
    }

    return summary_data, main_search


class Visitor_Manager:
    """
    Saves and Retrives website visitor information
    """
    def save_visit(self, request):
        get_ip = request.META.get('REMOTE_ADDR', None)
        visitor, created = Visitors.objects.get_or_create(visitor_ip=get_ip, defaults={'visit_count': 0})
        visitor.visit_count = F('visit_count') + 1
        visitor.save()

    def visit_reports(self):
        total_visits = Visitors.objects.aggregate(Sum('visit_count'))['visit_count__sum']
        return total_visits
