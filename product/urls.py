from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('contact/', views.contact, name="contact"),
    path('about/', views.about, name="about"),
    path('privacy/', views.privacy, name="privacy"),
    path('terms/', views.terms, name="terms"),    
    path("update/", views.add_scraped_data, name="update"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("my_products/", views.my_products, name="my_products"),
    path("my_history/", views.my_history, name="my_history"),
    path("<int:user_id>/tracked_product/<slug:product_id>/add/", views.track_product, name="track_product"),
    path("<int:user_id>/tracked_product/<slug:product_id>/remove/", views.untrack_product, name="untrack_product"),
    path("<int:user_id>/tracked_product/<slug:product_id>/delete/", views.delete_product, name="delete_product"),
    path("<int:user_id>/tracked_product/<slug:product_id>/search/", views.user_search, name="user_search"),
    # path("search/<slug:search_term>/", views.anonymouse_search, name="anonymouse_search"),
]
