
import requests
# from bs4 import BeautifulSoup as soup
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

# logging
logging.basicConfig(
    filename='/home/ex/Documents/GITLAB/ghost_modules/ghost_prices/test/wisepenny/spyders/classifieds.log', level=logging.INFO)

parser = cfg.ConfigParser()
parser.read("/home/ex/Documents/searchethio/Jobs/All_jobs/config.cfg")
# function to add to JSON


def write_json(new_data, file_name, cat_name):
    to_import = ["Jobs", "Seeking Work CVs"]
    if cat_name not in to_import:
        filename = "/home/ex/Documents/GITLAB/ghost_modules/ghost_prices/test/wisepenny/spyders/New_imports/" + file_name
        with open(filename, 'r+') as file:
            # First we load existing data into a dict.
            file_data = json.load(file)
            # Join new_data with file_data inside emp_details
            file_data["{}".format(cat_name)].append(new_data[0])
            # Sets file's current position at offset.
            file.seek(0)
            # convert back to json.
            json.dump(file_data, file, indent=4)
    else:
        with open("/home/ex/Documents/GITLAB/ghost_modules/ghost_prices/test/wisepenny/spyders/" + file_name, 'r+') as file:
            # First we load existing data into a dict.
            file_data = json.load(file)
            # Join new_data with file_data inside emp_details
            file_data["{}".format(cat_name)].append(new_data[0])
            # Sets file's current position at offset.
            file.seek(0)
            # convert back to json.
            json.dump(file_data, file, indent=4)


def parse_cats(json_file):
    # get cat_name, link, count, ttl_pages_per_cat
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
    with open('/home/ex/Documents/GITLAB/ghost_modules/ghost_prices/test/wisepenny/spyders/Category_tree.json', 'r') as g:
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
            # print(r.json())
            data = r.json()
            total_items = data['adverts_list']['count']
            total_pages = data['adverts_list']['total_pages']
            total_pages_per_cat[i] = [total_pages, total_items]
            time.sleep(1)
            break
    # print(colored(total_pages_per_cat, "red"))
    return total_pages_per_cat


def get_recent_items(s):
    with open('/home/ex/Documents/GITLAB/ghost_modules/ghost_prices/test/wisepenny/spyders/Category_tree.json', 'r') as g:
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
            # print(r.json())
            data = r.json()
            total_items = data['adverts_list']['in_day_count']
            if int(total_items) != 0:
                total_pages = ceil(int(total_items)/13)
            else:
                total_pages = 0
            total_pages_per_cat[i] = [total_pages, total_items]
            time.sleep(1)
            break
    # print(colored(total_pages_per_cat, "red"))
    return total_pages_per_cat


def get_listings(s):
    # ppc = pages_per_category
    with open('/home/ex/Documents/GITLAB/ghost_modules/ghost_prices/test/wisepenny/spyders/Total_items.json', 'r') as f:
        ppc = json.load(f)
    with open('/home/ex/Documents/GITLAB/ghost_modules/ghost_prices/test/wisepenny/spyders/Category_tree.json', 'r') as g:
        cat_tree = json.load(g)
    # new_ppc = 0
    # # Get latest listings
    # if int(ppc[i][0]) > 5:

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
                filename = "/home/ex/Documents/GITLAB/ghost_modules/ghost_prices/test/wisepenny/spyders/New_imports/" + "_{}_Listings.json".format(str(i).replace("&", "").replace(",", "").replace("  ", "_").replace(" ", "_"))
                with open(filename, 'w') as f:
                    json.dump(lst_per_cat, f)
                    print(colored("New Save to json 1 successful!", "green"))
            else:
                filename = "/home/ex/Documents/GITLAB/ghost_modules/ghost_prices/test/wisepenny/spyders/_{}_Listings.json".format(str(i).replace("&", "").replace(",", "").replace("  ", "_").replace(" ", "_"))
                with open(filename, 'w') as f:
                    json.dump(lst_per_cat, f)
                    print(colored("New Save to json 1 successful!", "green"))

        time.sleep(1)
        list_details = []
        lst_per_cat = {}

    # Append all listings into one file for import
    with open("/home/ex/Documents/GITLAB/ghost_modules/ghost_prices/test/wisepenny/spyders/[ALL] - Listings.json", 'w') as f:
        json.dump(all_lst, f)
    return lst_per_cat


def get_details(data, main_cat, s):
    list_cont = data['adverts_list']['adverts']
    listing_dict = {}
    for index, i in enumerate(list_cont):
        listing_url = "https://jiji.com.et/api_web/v1/item/{}".format(i['fb_view_content_data']['content_ids'])
        listing_headers = {
            'authority': 'jiji.com.et',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        }
        response = s.get(
            listing_url,
        )
        print(colored(response.json()['title'], "cyan"))

        try:
            ind = {"index": index}
            parent_cat = {"main_cat": main_cat}
            id = i['id']
            title = {"title": i['title']}
            cat_name = {"cat_name": i['category_name']}
            price = {"price": i['price_obj']['value']}
            city = {"city": i['region_parent_name']}
            sub_city = {"sub_city": i['region_name']}
            # if i['attrs']:
            #     if len(i['attrs']) > 0:
            #         attrs = {"attrs": [{x['name']:x['value']}
            #                            for x in i['attrs']]}
            # else:
            #     attrs = {"attrs": []}
            attrs = ""
            if i['attrs']:
                if len(i['attrs']) > 0:
                    for x in i['attrs']:
                        att = str(x['name']) + ": " + str(x['value']) + "<br>"
                        attrs+= att
            attrs = attrs.strip()
            print(colored(attrs, "red"))
            phone = {"phone": i['user_phone']}
            user_id = {"user_id": i['user_id']}
            status = {"status": i['status']}
            url = {"url": "https://jiji.com.et" + i['url']}
            if i['images']:
                if len(i['images']) > 0:
                    images = {"images": [x['url'] for x in i['images']][0]}
            else:
                images = {"images": []}
            listing_dict[id] = [ind, title, parent_cat, cat_name, price, city,
                                sub_city, attrs, phone, user_id, status, images, url]
        except Exception as e:
            print(
                colored("***Error crawling Listing - {}\n{}".format(i['id'], str(e)), "red"))
            continue
    return listing_dict

def indepth_details():
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

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:110.0) Gecko/20100101 Firefox/110.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://jiji.com.et/kolfe-keranio/mobile-phones/samsung-galaxy-s8-64-gb-black-Kjq72X4zexhkWLz7yINLBbP.html?page=1&pos=1&cur_pos=1&ads_per_page=20&ads_count=20&lid=G0YxqQeDqQMSDX2L',
        'X-CSRF-Token': 'IjBiYmEyZDA0MmRlMTM3MTVlODFhZTY0Y2NmYTBlMDM5ZWM5YjRlZmYi.ZCmBfw.HrrVVurKoeYn8WEnQ3J6LX37HQ0',
        'Content-Type': 'application/json',
        'Origin': 'https://jiji.com.et',
        'DNT': '1',
        'Proxy-Authorization': 'Basic MTpDaUpJUmpaaFpHUTJZelF6TkdSa1pUaGxPRE15TkRjek16TmpNV05pT1RGbE1tVTRFQUFZc1FNZ0NTZ0dNTnFHQXpvQ1ZWTlNEMjVsZEhkdmNtc3RaWGhoYlM1MWMxb0FnZ0VDWlc0PSR1bFA0My8rUFo2Nk1tZmpCTUVXS1JDN3lTV3puR3BXMGFmb1lwTGlWNXdYRVZNRlN5bkdBMXFvdm1CSW9OKytmMGNQMTdWbjJ1aUMwY2E0VU90TFVpOHBhTVAzVWcwd1FjWFBPQnl0WUhXNGpnaktXQjYrSTFSNVdxWUlZ',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
    }

    json_data = {
        'event_name': 'PageView',
        'event_id': 'bimoIwsu00FRKIc6GTBYfB',
        'event_source_url': 'https://jiji.com.et/kolfe-keranio/mobile-phones/samsung-galaxy-s8-64-gb-black-Kjq72X4zexhkWLz7yINLBbP.html?page=1&pos=1&cur_pos=1&ads_per_page=20&ads_count=20&lid=G0YxqQeDqQMSDX2L',
    }
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
        # print(sess_start.)
        if sess_start.status_code == 200:
            json_response = sess_start.json()
            # parse cat tree
            # print(colored("Parsing Cats ... ", "yellow"))
            # cat_tree = parse_cats(json_response)
            # # store cat tree
            # with open("Category_tree.json", 'w') as f:
            #     json.dump(cat_tree, f)
            # print(colored("Cats Parsed and Saved.", "green"))

            # # # parse location tree FOR LATER
            # print(colored("Parsing Loc ... ", "yellow"))
            # loc_tree = parse_regions(json_response)
            # # store loc tree
            # with open("Location_tree.json", 'w') as f:
            #     json.dump(loc_tree, f)
            # print(colored("Loc Parsed and Saved.", "green"))
            # # Get total items and total_pages for category links
            # print(colored("Parsing Items per Page ... ", "yellow"))
            # ttl_pages_per_cat = get_total_items(s)
            # # save total_pages per cat
            # with open("Total_items.json", 'w') as f:
            #     json.dump(ttl_pages_per_cat, f)
            # print(colored("Items per Page Parsed and Saved.", "green"))
            new_pages_per_cat = get_recent_items(s)
            # save total_pages per cat
            with open("/home/ex/Documents/GITLAB/ghost_modules/ghost_prices/test/wisepenny/spyders/Total_items.json", 'w') as f:
                json.dump(new_pages_per_cat, f)
            print(colored("New Items per Page Parsed and Saved.", "green"))

            # get details
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
    new_import_dir = "/home/ex/Documents/GITLAB/ghost_modules/ghost_prices/test/wisepenny/spyders/New_imports/"
    new_files = os.listdir("/home/ex/Documents/GITLAB/ghost_modules/ghost_prices/test/wisepenny/spyders/New_imports")
    available_updates = []
    for i in new_files:
        with open(new_import_dir + i, 'r') as f:
            new_uploads = json.load(f)
            if any(new_uploads.values()):
                available_updates.append(str(i))
    print(available_updates)
    test_ftp(new_import_dir, available_updates)


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


def process_import(id):
    cookies = {
        'wordpress_test_cookie': 'WP%20Cookie%20check',
    }

    headers_login = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:110.0) Gecko/20100101 Firefox/110.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://searchethio.com/wp-login.php?redirect_to=https%3A%2F%2Fsearchethio.com%2Fwp-admin%2F&reauth=1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://searchethio.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        # 'Cookie': 'wordpress_test_cookie=WP%20Cookie%20check',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        # Requests doesn't support trailers
        # 'TE': 'trailers',
    }

    dataa = 'log=ex&pwd=IjnfDBm%40FHllW%23*4YApPgPgz&wp-submit=Log+In&redirect_to=https%3A%2F%2Fsearchethio.com%2Fwp-admin%2F&testcookie=1'
    # dataa = {'log': 'ex', 'pwd': '8w6F TNrt bdPz IQpI m2F3 jelr'}
    wp_login = 'https://searchethio.com/wp-login.php'
    wp_admin = 'https://searchethio.com/wp-admin/'

    with requests.Session() as s:
        resp = s.post(wp_login, headers=headers_login, data=dataa, cookies=cookies)
        # print(resp.text)
        cookies = resp.cookies

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:110.0) Gecko/20100101 Firefox/110.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://searchethio.com/wp-admin/admin.php?page=pmxi-admin-manage&id=14&action=update',
            'X-Requested-With': 'XMLHttpRequest',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
        }

        trigger_url = "https://searchethio.com/wp-load.php?import_key=WF_3hU_&import_id={}&action=trigger".format(str(id))
        trigger = s.get(trigger_url, headers=headers)

        if trigger.status_code == 200:
            print("{} - Import trigger successful".format(str(id)))
        else:
            logging.info("{} - Import trigger failed with status code: ".format(str(id)), trigger.status_code)
        for j in range(20):
            while True:
                processing_url = "https://searchethio.com/wp-load.php?import_key=WF_3hU_&import_id={}&action=processing".format(str(id))

                process = s.get(processing_url, headers=headers)
                print(datetime.now())
                print(process)
                print("#" * 20)
                if process.status_code == 200:
                    print("[Import] {} [Run] {} - Processing in progress ...".format(id,j))
                    break
                else:
                    time.sleep(2)
        logging.info("Processing Complete!")
        s.close()


def failsafe():
    cookies = {
        'wordpress_test_cookie': 'WP%20Cookie%20check',
    }

    headers_login = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:110.0) Gecko/20100101 Firefox/110.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://searchethio.com/wp-login.php?redirect_to=https%3A%2F%2Fsearchethio.com%2Fwp-admin%2F&reauth=1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://searchethio.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        # 'Cookie': 'wordpress_test_cookie=WP%20Cookie%20check',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        # Requests doesn't support trailers
        # 'TE': 'trailers',
    }

    dataa = 'log=ex&pwd=IjnfDBm%40FHllW%23*4YApPgPgz&wp-submit=Log+In&redirect_to=https%3A%2F%2Fsearchethio.com%2Fwp-admin%2F&testcookie=1'
    wp_login = 'https://searchethio.com/wp-login.php'
    wp_admin = 'https://searchethio.com/wp-admin/'

    with requests.Session() as s:
        resp = s.post(wp_login, headers=headers_login, data=dataa)
        cookies = resp.cookies
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:110.0) Gecko/20100101 Firefox/110.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://searchethio.com/wp-admin/admin.php?page=pmxi-admin-manage&id=14&action=update',
            'X-Requested-With': 'XMLHttpRequest',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
        }
        for j in range(20):
            while True:
                processing_url = "https://searchethio.com/wp-load.php?import_key=WF_3hU_&import_id={}&action=processing".format(str(id))

                process = s.get(processing_url)
                print(datetime.now())
                print(process)
                print("#" * 20)
                if process.status_code == 200:
                    print("[Import] {} [Run] {} - Processing in progress ...".format(id,j))
                    break
                else:
                    time.sleep(2)
        logging.info("Processing Complete!")
        s.close()


try:
    logging.info("{}\n[Automation Started] [{}]".format(str("#"*50), str(datetime.now())))
    main()
    update_files()
    import_ids_processed = []
    # import_ids = [27]
    import_ids = [24, 29, 30, 31, 27, 26, 25, 23]
    random.shuffle(import_ids)
    for i in import_ids:
        if i not in import_ids_processed:
            process_import(str(i))
            import_ids_processed.append(i)
            logging.info("[Processed] {}".format(str(i)))
    logging.info("{}\n[Automation Ended] [{}]".format(str("#"*50), str(datetime.now())))
except Exception as e:
    logging.info(str(e))
    logging.info("{}\n[Automation Interrupted] [{}]".format(str("#"*50), str(datetime.now())))
