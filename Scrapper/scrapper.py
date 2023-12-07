from flask_cors import CORS
from flask import Flask, send_file, request
from selenium import webdriver  
import time, os, json
import requests
import pandas as pd
from Scrapper.headers import cat_codes, get_headers
# from headers import cat_codes, get_headers

from selenium.webdriver.chrome.service import Service

def get_data(urlPortal):    
    options = webdriver.chrome.options.Options()
    options.binary_location = "/usr/bin/google-chrome"
    # options = uc.ChromeOptions()
    options.add_argument("--no-sandbox")
#    options.add_argument("--disable-setuid-sandbox")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument('--headless')
    options.add_argument("--disable-gpu")
    options.add_argument('--remote-debugging-port=9222')
    service = Service(executable_path="/usr/bin/chromedriver") 
    
    driver = webdriver.Chrome(options=options) 
    driver.get(f'https://pbsystem.planetbids.com/portal/{urlPortal}/bo/bo-search')
    time.sleep(3)

    cookies = driver.get_cookies()

    driver.close()
    driver.quit()

    cookie_str = ''
    for cookie in cookies:
        name = cookie['name']
        value = cookie['value']
        cookie_str += f'{name}={value}; '

    s = requests.Session()
    headers = get_headers(urlPortal=urlPortal, cookie_str=cookie_str)
    data = s.get('https://pbsystem.planetbids.com/papi/version?new_session=true',headers=headers)
    data = data.json()
    visitId = data['data']['attributes']['visitId']
    
    new_headers = get_headers(urlPortal, cookie_str, visitId)

    stage_id = 3 #change to 3 for bidding only

    final = []

    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))

    codes_search_string = ''
    # for code in cat_codes['CODES']:
    #     codes_search_string+= f"&category_ids%5B%5D={code}"

    for page in range(1,4):
        
        new_url = f'https://pbsystem.planetbids.com/papi/bids?bid_type_id=0{codes_search_string}&cid={urlPortal}&dept_id=0&due_date_from=&due_date_to=&keyword=&page={str(page)}&per_page=30&sort_by=&sort_order=-1&stage_id={str(stage_id)}'
        
        new_headers['path'] = f'/papi/bids?bid_type_id=0{codes_search_string}&cid={urlPortal}&dept_id=0&due_date_from=&due_date_to=&keyword=&page={str(page)}&per_page=30&sort_by=&sort_order=-1&stage_id={str(stage_id)}'
        info = s.get(new_url,headers=new_headers).json()
        print(f'Scaping page: {page}')

        for bid in info['data']:
            new_dict = bid['attributes']
            new_dict['page_scrape'] = page
            bid_url = f'https://pbsystem.planetbids.com/portal/{urlPortal}/bo/bo-detail/' + str(bid['id'])
            header_for_est_bid_amount = new_headers
            header_for_est_bid_amount['referer'] = bid_url
            bid_info = s.get(f"https://pbsystem.planetbids.com/papi/bid-details/{str(bid['id'])}",headers=header_for_est_bid_amount).json()
            try:
                new_dict['estimatedBid'] = bid_info['data']['attributes']['estimatedValue']
                new_dict['County'] = bid_info['data']['attributes']['county']
            except:
                new_dict['estimatedBid'] = 'Not Found'
            new_dict['CategoriesList'] = []
            for cats in bid_info['included']:    
                new_dict['CategoriesList'].append((cats['id'] + ' - ' + cats['attributes']['categoryName']))
            new_dict['url'] = bid_url
            final.append(new_dict)

        return final
    
