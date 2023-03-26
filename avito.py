from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
from python_tokens import tokens
import time
import json

# print(tokens)
URL = 'https://www.avito.ru/samarskaya_oblast/doma_dachi_kottedzhi/prodam-ASgBAgICAUSUA9AQ?context=H4sIAAAAAAAA_0q0MrSqLraysFJKK8rPDUhMT1WyLrYyNLJSKk4sS02JL05NLErOULKuBQQAAP__IWhYLCkAAAA&f=ASgBAQECAUSUA9AQA0DYCDTMWcpZzlmQvQ5E9qTRAfSk0QHypNEB8KTRAcq9DhSwnJQCAUXGmgwWeyJmcm9tIjowLCJ0byI6OTAwMDAwfQ&s=104'
PAUSE_DURATION_SECONDS = 5
TOKEN = tokens["token"]
CHAT_ID = tokens["chat_id"]
SEND_URL = f'https://api.telegram.org/bot{TOKEN}/sendMessage'

houses_list = []
houses_sended_list = []



def main():
    driver.get(URL)
    sleep(PAUSE_DURATION_SECONDS)
    # driver.find_element(by=By.CLASS_NAME, value='iva-item-body-KLUuy')
    soup = BeautifulSoup(driver.page_source, "lxml")
    houses = soup.find_all("div", class_="iva-item-body-KLUuy")
    with open('data.txt') as old_data_file:
        old_data = json.loads(old_data_file.read())["link"]
    for house in houses:
        a = house.find("a").get("href")
        link_house_result = f"https://www.avito.ru/{a}"
        link_object = {
            "link_of_house": link_house_result
            }
        if link_object not in old_data:
            send_list(link_house_result)
            old_data.append(link_object)
    with open('data.txt', 'a') as file:
        json.dump(old_data, file)


def send_list(house):
    requests.post(SEND_URL, json={
                  'chat_id': CHAT_ID, 'text': str(house)})


if __name__ == '__main__':
    while (True):
        try:
            service = Service(executable_path=ChromeDriverManager().install())
            driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')
                        #   for windows:
                        # driver = webdriver.Chrome(service=service)
            
            main()
        except Exception as e:
            print(e)
        finally:
            time.sleep(10)
            driver.quit()
        time.sleep(1000)
