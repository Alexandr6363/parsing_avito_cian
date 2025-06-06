from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
from python_tokens import tokens
import time
import json


URL_CIAN = 'https://samara.cian.ru/cat.php?currency=2&deal_type=sale&drainage=1&electricity=1&engine_version=2&gas=1&is_dacha=0&maxprice=1500000&object_type%5B0%5D=1&offer_type=suburban&region=4608&sort=creation_date_desc&water=1&wc_site=1'
URL = 'https://www.avito.ru/samarskaya_oblast/doma_dachi_kottedzhi/prodam/do-1500000-rubley-ASgBAgECAUSUA9AQAUXGmgwXeyJmcm9tIjowLCJ0byI6MTUwMDAwMH0?f=ASgBAQECAUSUA9AQAkDYCDTMWcpZzlmQvQ5E9qTRAfSk0QHypNEB8KTRAQFFxpoMF3siZnJvbSI6MCwidG8iOjE1MDAwMDB9&s=104'
PAUSE_DURATION_SECONDS = 5
TOKEN = tokens["token"]
CHAT_ID = tokens["chat_id"]
SEND_URL = f'https://api.telegram.org/bot{TOKEN}/sendMessage'


def set_chrome_options() -> Options:
    """Sets chrome options for Selenium.
    Chrome options for headless browser is enabled.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    return chrome_options

def avito_scan(driver):
    driver.get(URL)
    sleep(PAUSE_DURATION_SECONDS)
    soup = BeautifulSoup(driver.page_source, "lxml")
    houses = soup.find_all("div", class_="iva-item-body-KLUuy")
    data_list = []
    for house in houses:
        a = house.find("a").get("href")
        link_house_result = f"https://www.avito.ru{a}"
        data_list.append(link_house_result)
    write_and_send(data_list, 'data/data.txt')



def cian_scan(driver):
    driver.get(URL_CIAN)
    sleep(PAUSE_DURATION_SECONDS)
    soup = BeautifulSoup(driver.page_source, "lxml")
    houses = soup.find_all("a", class_="_93444fe79c--link--eoxce")
    data_list = []
    for house in houses:
        link_house_result = house.get("href")
        data_list.append(link_house_result)
    write_and_send(data_list, 'data/data_cian.txt')


def write_and_send(data_list, file):
    with open(file, "r+") as data_file:
        if data_file:
            old_data = json.load(data_file)
        for link_house_result in data_list:
            link_object = {
                "link_of_house": link_house_result
            }
            if link_object not in old_data:
                send_list(link_house_result)
                old_data.append(link_object)
        data_file.seek(0)
        json.dump(old_data, data_file, indent=4)
        data_file.truncate()


def send_list(house):
    requests.post(SEND_URL, json={
                  'chat_id': CHAT_ID, 'text': str(house)})


def main(scan_function):
    try:
        driver = webdriver.Chrome(options=set_chrome_options())
                    #   for windows:
                    # driver = webdriver.Chrome(service=service)            
        scan_function(driver)
    except Exception as e:
        # send_list(e)
        print(e)
    finally:
        time.sleep(1)
        driver.quit()
    time.sleep(500)


if __name__ == '__main__':
    # service = Service(executable_path=ChromeDriverManager().install())
    while (True):
        main(avito_scan)
        main(cian_scan)
