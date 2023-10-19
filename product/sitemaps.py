# sitemaps.py
from django.contrib import sitemaps
from django.urls import reverse


class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'weekly'

    def items(self):
        return ['home', 'contact', 'login', 'register', 'privacy', 'terms', 'about']

    def location(self, item):
        return reverse(item)
