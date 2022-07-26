import selenium
from selenium import webdriver
import pandas as pd
from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import time
import uuid
import os
import urllib
import json
from json import JSONEncoder
from uuid import UUID

global Postcode
Postcode = "BT4"

class Scraper:
    def __init__(self, url: str = 'https://www.propertypal.com') -> None:
        self.driver = Chrome(ChromeDriverManager().install())
        self.driver.get(url)
        
    def ivan_accept_cookies(self, xpath:str = '//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]'):
        
        try:
            time.sleep(1)
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))

            button = self.driver.find_element(By.XPATH, xpath)
            button.click()
        except TimeoutException:
            print("No Cookies Found")

    def accept_cookies(self, xpath:str = '//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]'):
        button = self.driver.find_element(By.XPATH, xpath)
        button.click()

    
    def search_word(self, xpath, pc = Postcode):

        search = self.driver.find_element(By.XPATH, xpath)
        self.driver.implicitly_wait(10)
        ActionChains(self.driver).move_to_element(search).click(search).perform()
        ActionChains(self.driver).send_keys(pc).perform()

    def scroll_down(self):
        
        self.driver.execute_script("window.scrollTo(0, 540)") 
    
    def search_rent(self):
        rent = self.driver.find_element_by_xpath('//*[@id="searchForm"]/div/div[2]/button[2]')
        rent.click()

    def search_sale(self):
        rent = self.driver.find_element_by_xpath('//*[@id="searchForm"]/div/div[2]/button[1]')
        rent.click()

    def button_click(self,xpath):
        button = self.driver.find_element_by_xpath(xpath)
        button.click()
    
    def find_container(self, xpath: str = '//*[@id="body"]/div[3]/div/div[1]/div/ul'):
        self.container = self.driver.find_element(By.XPATH, xpath)
        return self.container

##
# NAVIGATE THE WEBSITE
##

if __name__ == "__main__":
    bot = Scraper()
    bot.ivan_accept_cookies()
    time.sleep(2)
    bot.button_click('//a[@href="/login"]')
    time.sleep(2)
    bot.search_word('//input[@placeholder="Email address"]','sopranotony233@gmail.com')
    time.sleep(2)
    bot.search_word('//input[@placeholder="Password"]','sopranotony321')
    time.sleep(2)
    bot.button_click('//*[@id="root"]/div/div/div/div/div/div[1]/div/div[2]/div[2]/form/button')
    time.sleep(2)
    bot.button_click('//a[@class="mainnav-logo"]')  
    time.sleep(2)
    bot.search_word('//*[@id="searchForm"]/div/div[1]')
    time.sleep(2)
    bot.search_rent()
    time.sleep(2)
    

    #CREATE THE LIST OF LINKS
    list_links = []
    print("Finding elements...")
    while True:
        container = bot.find_container()
        items = container.find_elements(By.XPATH, './li')
        for i in items:
            try:
                house = i.find_element(By.XPATH, './/a[2]')
                link = house.get_attribute('href')
                list_links.append(link)
            except:
                print("no href found")
        
        try:
            bot.button_click('//a[@class="btn paging-next"]')
        except NoSuchElementException:
            print("end of list")
            break

    #GRAB INFO FROM EACH LINK AND STORE
    print("Grabbing info...")
    prop_dict = {"fr-id": [],
            "id": [],
            "Link": [],
             "Summary": [],
            "Address": [],
            "Price": [],
            "Image links": []
            }
    for link in list_links:
        im = link[-6:]
        im2 = link[28:35]
        prop_dict["fr-id"].append(im2+im)
        id = uuid.uuid4()
        prop_dict["id"].append(id)
        bot.driver.get(link)
        prop_dict["Link"].append(link)
        time.sleep(1)
        summary = bot.driver.find_element(By.XPATH, '//div[@class="prop-heading-brief"]')
        prop_dict["Summary"].append(summary.text)
        time.sleep(1)
        info = bot.driver.find_element(By.XPATH, '//div[@class="prop-summary-row"]')
        address = info.find_element(By.XPATH, './/h1')
        prop_dict["Address"].append(address.text)
        time.sleep(1)
        price = bot.driver.find_element(By.XPATH, '//div[@class="prop-price"]')
        prop_dict["Price"].append(price.text)
        img_list = []
        img_container = bot.driver.find_elements(By.XPATH, '//div[@class="Slideshow-slides SlideshowCarousel"]//img')
        img_list += img_container

    img_links = []
    for img in img_list:
        try:
            link = img.get_attribute('src')
            img_links.append(link)
        except:
            print('No src found')
    prop_dict["Image links"].append(img_links)


    os.mkdir(f"/Users/ryanhughes/Desktop/Aicore/Property-Pal-Pipeline-/Property_Photos/{Postcode}")
    image_directory = os.path.dirname(f"/Users/ryanhughes/Desktop/Aicore/Property-Pal-Pipeline-/Property_Photos/{Postcode}/")
    img_link_ct=0
    for i in prop_dict["Image links"]:
        img_link_ct += 1
        img_ct = 0
        for url in i:
            try:
                img_ct += 1
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with open(f"{image_directory}/{prop_dict['fr-id'][img_link_ct]}_{str(img_ct)}.jpg", "wb") as f:
                    with urllib.request.urlopen(req) as r:
                        f.write(r.read())
            except IndexError:
                pass 

    old_default = JSONEncoder.default

    def new_default(self, obj):
        if isinstance(obj, UUID):
            return str(obj)
        return old_default(self, obj)

    JSONEncoder.default = new_default
 
    with open(f'/Users/ryanhughes/Desktop/Aicore/Property-Pal-Pipeline-/raw_data/{Postcode}.json', 'w') as f:
        json.dump(prop_dict, f)

    df = pd.DataFrame(prop_dict)

