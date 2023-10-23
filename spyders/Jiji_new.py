import requests
import json
from termcolor import colored
import time
from math import ceil
import os
import shutil
import configparser as cfg
import base64
import ftplib
import logging
from datetime import datetime
import random
from pytz import timezone
import pytz
logging.basicConfig(
    filename='classifieds.log', level=logging.INFO)

parser = cfg.ConfigParser()
parser.read("hidden/config.cfg")


def parse_datetime_jiji(datetime_string):
    input_datetime_str = datetime_string
    parsed_datetime = datetime.strptime(input_datetime_str, "%a, %d %b %Y %H:%M:%S %Z")
    parsed_datetime_utc = parsed_datetime.astimezone(pytz.UTC)
    iso8601_datetime_str = parsed_datetime_utc.strftime("%Y-%m-%dT%H:%M:%S.%f%z").replace("+0000", "+00:00")
    return iso8601_datetime_str

def write_json(new_data, file_name, cat_name):
    to_import = ["Jobs", "Seeking Work CVs"]
    if cat_name not in to_import:
        filename = "./New_imports/" + file_name
        with open(filename, 'r+') as file:
            file_data = json.load(file)
            file_data["{}".format(cat_name)].append(new_data[0])
            file.seek(0)
            json.dump(file_data, file, indent=4)
    else:
        with open("./" + file_name, 'r+') as file:
            file_data = json.load(file)
            file_data["{}".format(cat_name)].append(new_data[0])
            file.seek(0)
            json.dump(file_data, file, indent=4)


def parse_cats(json_file):
    cat_data = {}
    for i in range(len(json_file['data'])):
        cont = json_file['data']['categories'][i]
        cat_name = cont['name']
        cat_slug = cont['slug']
        sub_cat_array = []
        if cont['childes'] != []:
            for j in range(len(cont['childes'])):
                sc_cont = cont['childes'][j]
                sc_name = sc_cont['name']
                sc_id = sc_cont['id']
                sc_slug = sc_cont['slug']
                sub_cat_array.append({sc_name: [sc_id, sc_slug]})
        cat_data[cat_name] = {cat_slug: sub_cat_array}
    return(cat_data)


def parse_regions(json_file):
    loc_data = {}
    for j in range(1, 12):
        sub_loc_array = []
        loc_name = ""
        for i in json_file['data']['regions']:
            if j == i['id']:
                loc_name = i['name']

            if j == i['parent_id']:
                sub_loc = i['name']
                sub_loc_array.append(sub_loc)
        loc_data[loc_name] = sub_loc_array
    return(loc_data)


def get_total_items(s):
    with open('./Category_tree.json', 'r') as g:
        cat_tree = json.load(g)
    total_pages_per_cat = {}
    for i, j in cat_tree.items():
        time.sleep(1)
        for a, b in j.items():
            headers = {
                'authority': 'jiji.com.et',
                'accept': 'application/json, text/plain, */*',
                'accept-language': 'en-US,en;q=0.7',
                'referer': 'https://jiji.com.et/' + str(a),
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'sec-gpc': '1',
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
            }
            params = {
                'slug': str(a),
                'init_page': 'true',
                'page': '1',
                'webp': 'true',
            }

            r = s.get('https://jiji.com.et/api_web/v1/listing',
                      params=params, headers=headers)
            data = r.json()
            total_items = data['adverts_list']['count']
            total_pages = data['adverts_list']['total_pages']
            total_pages_per_cat[i] = [total_pages, total_items]
            time.sleep(1)
            break
    return total_pages_per_cat


def get_recent_items(s):
    with open('./Category_tree.json', 'r') as g:
        cat_tree = json.load(g)
    total_pages_per_cat = {}
    for i, j in cat_tree.items():
        time.sleep(1)
        for a, b in j.items():
            headers = {
                'authority': 'jiji.com.et',
                'accept': 'application/json, text/plain, */*',
                'accept-language': 'en-US,en;q=0.7',
                'referer': 'https://jiji.com.et/' + str(a),
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'sec-gpc': '1',
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
            }
            params = {
                'slug': str(a),
                'init_page': 'true',
                'page': '1',
                'webp': 'true',
            }

            r = s.get('https://jiji.com.et/api_web/v1/listing',
                      params=params, headers=headers)
            data = r.json()
            total_items = data['adverts_list']['in_day_count']
            if int(total_items) != 0:
                total_pages = ceil(int(total_items)/13)
            else:
                total_pages = 0
            total_pages_per_cat[i] = [total_pages, total_items]
            time.sleep(1)
            break
    return total_pages_per_cat


def get_listings(s):
    with open('./Total_items.json', 'r') as f:
        ppc = json.load(f)
    with open('./Category_tree.json', 'r') as g:
        cat_tree = json.load(g)
    lst_per_cat = {}
    list_details = []
    all_lst = {}
    for i, j in cat_tree.items():
        lst_per_cat[str(i)] = []
        cat_name = str(i)
        for a, b in j.items():
            time.sleep(1)
            for x in range(1, int(ppc[i][0]) + 1):
                try:
                    print(
                        colored("Category - [{}] ### Page - [{} / {}]".format(i, x, int(ppc[i][0]) + 1), "green"))
                    headers = {
                        'authority': 'jiji.com.et',
                        'accept': 'application/json, text/plain, */*',
                        'accept-language': 'en-US,en;q=0.7',
                        'referer': 'https://jiji.com.et/' + str(a),
                        'sec-fetch-dest': 'empty',
                        'sec-fetch-mode': 'cors',
                        'sec-fetch-site': 'same-origin',
                        'sec-gpc': '1',
                        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
                    }
                    params = {
                        'slug': str(a),
                        'init_page': 'true',
                        'page': str(x),
                        'webp': 'true',
                        'sort': 'new',
                    }

                    r = s.get('https://jiji.com.et/api_web/v1/listing',
                              params=params, headers=headers)
                    if r.status_code == 200:
                        data = r.json()
                        list_det = get_details(data, str(i), s)
                        list_details.append(list_det)
                    else:
                        print(colored("Error Crawling page - {}".format(x), "red"))

                except Exception as e:
                    print(
                        colored("Error crawling page - {}\n{}".format(x, str(e)), "red"))
                    continue
                time.sleep(1)
            time.sleep(1)
        lst_per_cat[cat_name] = list_details
        all_lst[cat_name] = list_details
        try:
            write_json(
                lst_per_cat, "_{}_Listings.json".format(str(i).replace("&", "").replace(",", "").replace("  ", "_").replace(" ", "_")), str(i))

        except Exception as e:
            print(colored("Error saving to json 1\n{}".format(str(e)), "red"))
            to_import = ["Jobs", "Seeking Work CVs"]
            if str(i) not in to_import:
                filename = "./New_imports/" + "_{}_Listings.json".format(str(i).replace("&", "").replace(",", "").replace("  ", "_").replace(" ", "_"))
                with open(filename, 'w') as f:
                    json.dump(lst_per_cat, f)
                    print(colored("New Save to json 1 successful!", "green"))
            else:
                filename = "./_{}_Listings.json".format(str(i).replace("&", "").replace(",", "").replace("  ", "_").replace(" ", "_"))
                with open(filename, 'w') as f:
                    json.dump(lst_per_cat, f)
                    print(colored("New Save to json 1 successful!", "green"))

        time.sleep(1)
        list_details = []
        lst_per_cat = {}

    # Append all listings into one file for import
    with open("./[ALL] - Listings.json", 'w') as f:
        json.dump(all_lst, f)
    return lst_per_cat


def get_details(data, main_cat, s):
    list_cont = data['adverts_list']['adverts']
    listing_dict = {}
    for index, i in enumerate(list_cont):
        time.sleep(0.7)
        listing_url = "https://jiji.com.et/api_web/v1/item/{}".format(i['fb_view_content_data']['content_ids'][0])
        print(colored(listing_url, "cyan"))
        listing_headers = {
            'authority': 'jiji.com.et',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        }
        response = s.get(
            listing_url        )
        print(colored(response.json()['advert'], "cyan"))
        key = response.json()['advert']
        try:
            ind = {"index": index}
            parent_cat = {"main_cat": main_cat}
            id = key['id']
            title = {"title": key['title']}
            cat_name = {"cat_name": key['category_name']}
            price = {"price": key['price_obj']['value']}
            city = {"city": key['region_text'].split(",")[0].strip()}
            sub_city = {"sub_city": key['region_name']}
            attrs_dict = {}
            attrs_array = []
            if key['attrs']:
                if len(key['attrs']) > 0:
                    a = {}
                    for x in key['attrs']:
                        a[x['name']] = x['value']
                    attrs_array.append(a)
            attrs_dict["attrs"] = attrs_array
            print(colored(attrs_array, "red"))

            phone = {"phone": i['user_phone']}
            user_id = {"user_id": i['user_id']}
            status = {"status": key['status']}
            source = {"source": "Jiji"}
            print(colored("{} - {} - {}".format(key['date'], key['date_created'], key['date_moderated']), "cyan"))
            date_added = {"date_added": parse_datetime_jiji(key['date_created'])}
            date_scraped = {"date_scraped": datetime.now(timezone('UTC')).isoformat()}
            print(date_added, date_scraped)
            url = {"url": key['url']}
            if key['images_data']['base']:
                if len(key['images_data']['base']) > 0:
                    images = {"images": [x.get('url') for x in key['images_data']['base'] if x.get('is_main') == True][0]}
            else:
                images = {"images": []}
            print(colored("images - {}".format(images), "cyan"))
            listing_dict[id] = [ind, title, parent_cat, cat_name, price, city,
                                sub_city, attrs_dict, phone, user_id, status, images, url, source, date_added, date_scraped]
        except Exception as e:
            print(
                colored("***Error crawling Listing - {}\n{}".format(key['id'], str(e)), "red"))
            continue
    return listing_dict


def main():
    headers = {
        'authority': 'jiji.com.et',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.7',
        'cache-control': 'max-age=0',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'sec-gpc': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    }
    start = "https://jiji.com.et/"
    start_api = "https://jiji.com.et/api_web/v1/start_spa_data"

    with requests.Session() as s:
        sess_start = s.get(start_api, headers=headers)
        print(sess_start.status_code)
        if sess_start.status_code == 200:
            new_pages_per_cat = get_recent_items(s)
            with open("./Total_items.json", 'w') as f:
                json.dump(new_pages_per_cat, f)
            print(colored("New Items per Page Parsed and Saved.", "green"))

            print(colored("Getting Details ... ", "yellow"))
            try:
                get_listings(s)
            except Exception as e:
                print(colored("Error getting Listings\n{}".format(str(e)), "red"))

            print(colored("Details Saved.", "green"))

        else:
            print(colored("Error in connection to main site", "red"))
            s.close()


def update_files():
    new_import_dir = "./New_imports/"
    new_files = os.listdir("./New_imports")
    available_updates = []
    for i in new_files:
        with open(new_import_dir + i, 'r') as f:
            new_uploads = json.load(f)
            if any(new_uploads.values()):
                available_updates.append(str(i))
    print(available_updates)
    # test_ftp(new_import_dir, available_updates)


def test_ftp(origin_dir, available_updates):
    print("Transferring Files ... ")
    host = base64.b64decode(parser.get(
        'qcreds', 'ft_h')).decode('utf-8')
    username = base64.b64decode(parser.get(
        'qcreds', 'ft_u')).decode('utf-8')
    p_w = base64.b64decode(parser.get(
        'qcreds', 'ft_p')).decode('utf-8')

    session = ftplib.FTP(host,
                         username, p_w)

    for i in available_updates:
        try:
            updates = open(
                origin_dir + str(i), 'rb')
            if updates:
                print("{} - Updates Found!".format(str(i)))
                # delete existing users file
                try:
                    session.delete("{}".format(str(i)))
                except Exception as e:
                    logging.info("Error Deleting Existing -- {} -- Updates -- \n".format(str(i)) + str(e))
                try:
                    session.storbinary('STOR {}'.format(str(i)),
                                       updates)     # send the file
                except Exception as e:
                    logging.info("Error adding jobs to server -- " + str(e))
                updates.close()
                logging.info("Transferred {}!".format(str(i)))
        except Exception as e:
            logging.info("No {} found on local drive! --- \n".format(str(i)) + str(e))
            pass

    # close file and FTP
    session.quit()
    logging.info("File Transfer Complete! - " + str(datetime.now()))



try:
    logging.info("{}\n[Automation Started] [{}]".format(str("#"*50), str(datetime.now())))
    main()
    update_files()
    logging.info("{}\n[Automation Ended] [{}]".format(str("#"*50), str(datetime.now())))
except Exception as e:
    logging.info(str(e))
    logging.info("{}\n[Automation Interrupted] [{}]".format(str("#"*50), str(datetime.now())))
