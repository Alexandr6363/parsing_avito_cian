from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
from python_tokens import tokens
import time

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

    for house in houses:
        public_time = house.find("div", class_="date-text-KmWDf text-text-LurtD text-size-s-BxGpL text-color-noaccent-P1Rfs").text
        a = house.find("a").get("href")
        if "час" in public_time:
            link_house_result = f"https://www.avito.ru/{a}"
            houses_list.append(link_house_result)
            if (link_house_result in houses_list) & (link_house_result not in houses_sended_list):
                send_list(link_house_result)
                houses_sended_list.append(link_house_result)
#     get_phone_number(houses_list)


# def get_phone_number(houses_list):
#     if houses_list:
#         tab = 2
#         for link in houses_list:
#             time.sleep(1)
#             driver.execute_script(f"window.open('about:blank', {tab});")
#             driver.switch_to.window(f"{tab}")
#             driver.get(link)

#             tab += 1
    



def send_list(houses_list):
    requests.post(SEND_URL, json={'chat_id': CHAT_ID, 'text': str(houses_list)}) 




if __name__ == '__main__':
    while (True):        
        try:
            service = Service(executable_path=ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service)
            main()
        except Exception as e:
            print(e)
        finally:
            time.sleep(10)
            driver.quit()
        time.sleep(1000)



