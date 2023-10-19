from . import utils
from .utils import Visitor_Manager, SearchQuery_Manager
from .forms import SearchForm, SubscribeForm, ContactForm
from .models import Category, Product, PriceSource, SearchQuery, Subscribers, ProductTracker
from ast import literal_eval
from django.core.management import call_command
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.mail import send_mail
from django.db.models import Q, Count
from django.db.utils import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect
import json
from termcolor import colored


def about(request):
    return render(request, "product/about.html")
def terms(request):
    return render(request, "product/terms.html")
def privacy(request):
    return render(request, "product/privacy.html")    

def contact(response):
    if response.method == 'POST':
        form = ContactForm(response.POST)
        if form.is_valid():
            sender_name = form.cleaned_data["full_name"]
            sender_email = form.cleaned_data['email']
            sender_phone = form.cleaned_data['phone']
            sender_message = form.cleaned_data['message']

            send_mail(
                f"{sender_name} - [WisePenny]",  # Subject
                # Message
                f"*********************************\nFrom - [{sender_name}]\nEmail - [{sender_email}]\nPhone - [{sender_phone}]\n*********************************\n\nMessage\n" + sender_message,
                sender_email,  # From Email
                ['contact@m-ini.me'],  # To Email
            )

            return render(response, "product/contact.html", {'message_name': f"Thank You {sender_name}!"})
    else:
        form = ContactForm()
    return render(response, "product/contact.html", {'form': form})

def home(request):
    vm = Visitor_Manager()
    vm.save_visit(request)
    ttl_visitors = vm.visit_reports()
    print(colored(ttl_visitors, "green"))
    summary_data = None
    g_data = None
    all_data, results_1 = utils.get_all_data()
    g_data = all_data
    search_term = None
    results_1 = None
    user_searches = None
    recent_searches = SearchQuery_Manager().search_reports()
    if request.user.is_authenticated:
        user_searches = ProductTracker.objects.select_related('user').filter(user=request.user)


    if request.method == "POST":
        search_form = SearchForm(request.POST, auto_id=True)
        sub_form = SubscribeForm(request.POST, auto_id=True)
        if 'search' in request.POST and search_form.is_valid():
            search_term = search_form.cleaned_data["search_term"]

            print(colored(summary_data, "green"))
            # store in SearchQuery
            SearchQuery_Manager(search_term).save_search(request)

            if search_term:
                summary_data, results_1 = utils.get_summary_data(search_term)
                if request.user.is_authenticated:
                    pt, created = ProductTracker.objects.get_or_create(user=request.user, name=search_term)

        if "subscribee" in request.POST and sub_form.is_valid():
            subs_email = sub_form.cleaned_data['sub_form']
            try:
                sf = Subscribers(sub_email=subs_email)
                sf.save()
                send_mail(
                    f"WisePenny - Thanks for Subscribing!",  # Subject
                    "Thank you for subscribing!\nI will be sending you updates on new products and price changes as they go online!\nI hope you enjoy the free service.\n\n\nEskias Yilma\nFounder & CEO\nWisePenny",  # Message
                    'contact@m-ini.me',  # "ghostexus@gmail.com",  # From Email
                    [subs_email],  # To Email
                )
                messages.success(
                    request, "Thanks for Subscribing! Goodies are on their way!")
            except Exception as e:
                print(colored(str(e), "red"))
                messages.success(
                    request, "You are already a subscriber! Kuddos!")
            return redirect(home)

    else:
        search_form = SearchForm()
        sub_form = SubscribeForm()

    return render(request, "product/home.html", {
        "form":search_form,
        "results_1":results_1,
        "recent_searches":recent_searches,
        "ttl_visitors":ttl_visitors,
        "sub_form":sub_form,
        "summary_data":summary_data,
        "all_data":g_data,
        "user_searches":user_searches,
        "search_term":search_term,
        })


# Management commands routes
@user_passes_test(lambda u: u.is_superuser)
def add_scraped_data(request):
    call_command('add_mekina_data')
    call_command('add_jiji_data')
    return HttpResponse("Custom management commands executed.")


# User Dashboard
@ login_required(login_url='/login/')
def dashboard(request):
    """
    User Dashboard to Track Products
    """
    utils.Visitor_Manager().save_visit(request)
    ttl_visitors = utils.Visitor_Manager().visit_reports()
    # search_reports = utils.SearchQuery_Manager().search_reports()
    summary_data = None
    all_data = utils.get_summary_data("")
    search_term = None
    results_1 = None

    if request.method == "POST":
        search_form = SearchForm(request.POST, auto_id=True)
        if 'search' in request.POST and search_form.is_valid():
            search_term = search_form.cleaned_data["search_term"]

            print(colored(summary_data, "green"))
            # store in SearchQuery
            SearchQuery_Manager(search_term).save_search(request)
            # print(search_term)
            if search_term:
                summary_data, results_1 = utils.get_summary_data(search_term)
                try:
                    pt, created = ProductTracker.objects.get_or_create(user=request.user, name=search_term)
                    # pt.save()
                except IntegrityError:
                    pass

        else:
            messages.success(
                request, "Please Login or Create a Free Account to Shorten Links.")
            return redirect(home)

    else:
        search_form = SearchForm()
    user_searches = ProductTracker.objects.select_related('user').filter(user=request.user)
    tracked_searches = user_searches.filter(tracked=True)
    print(colored(tracked_searches, "blue"))
    return render(request, "product/dashboard.html", {
        "form":search_form,
        "results_1":results_1,
        # "recent_searches":search_reports,
        "ttl_visitors":ttl_visitors,
        "summary_data":summary_data,
        "all_data":all_data,
        "tracked_products":tracked_searches,
        "user_searches":user_searches
        })

@ login_required(login_url='/login/')
def my_products(request):
    products = ProductTracker.objects.filter(user=request.user)
    return render(request, "product/my_products.html", {'products':products})

@ login_required(login_url='/login/')
def my_history(request):
    return render(request, "product/my_history.html")

@ login_required(login_url='/login/')
def track_product(request, user_id, product_id):
    try:
        to_add = ProductTracker.objects.get(id=product_id)
        to_add.tracked = True
        to_add.save()
        messages.success(request, "Tracker Updated Successfully!")
    except IntegrityError:
        messages.success(request, "Tracker Update Failed! Please try Again.")
    return redirect('my_products')


@ login_required(login_url='/login/')
def untrack_product(request, user_id, product_id):
    try:
        to_add = ProductTracker.objects.get(id=product_id)
        to_add.tracked = False
        to_add.save()
        messages.success(request, "Tracker Updated Successfully!")
    except IntegrityError:
        messages.success(request, "Tracker Update Failed! Please try Again.")
    return redirect('my_products')

@ login_required(login_url='/login/')
def delete_product(request, user_id, product_id):
    try:
        to_add = ProductTracker.objects.get(id=product_id)
        to_add.delete()
        messages.success(request, "Tracker Updated Successfully!")
    except IntegrityError:
        messages.success(request, "Tracker Update Failed! Please try Again.")
    return redirect('my_products')

@ login_required(login_url='/login/')
def user_search(request, user_id, product_id):
    products = ProductTracker.objects.get(id=product_id)
    return render(request, "product/search_results.html", {'products':products})
