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
from Scraper import Scraper

global Postcode
Postcode = "BT1"

# NAVIGATE THE WEBSITE

#This block uses a dummy email to log into the website, which avoids problems further down the line

class PropertyScraper(Scraper):

    def __init__(self, url: str = 'https://www.propertypal.com', headless: bool = False):
        super().__init__(url, headless)

    def login(self, bot = Scraper()):
        bot 
        bot.accept_cookies()
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

#We first find the container with which the links for each page are located, in the form of href
    def get_links(self, bot = Scraper):
        list_links = []
        print("Finding elements...")
        while True:
            container = bot.find_container(self)
            items = container.find_elements(By.XPATH, './li')
            for i in items:
                try:
                    house = i.find_element(By.XPATH, './/a[2]')
                    link = house.get_attribute('href')
                    list_links.append(link)
                except:
                    print("no href found")
            
            try:
                Scraper.button_click('//a[@class="btn paging-next"]')
            except NoSuchElementException:
                print("end of list")
                break
            return list_links

#GRAB INFO FROM EACH LINK AND STORE

#We now iterate through our list of links, and grab our desired info, and store it into a dictionary.

    def get_info(self):
        print("Grabbing info...")
        prop_dict = {"fr-id": [],
                "id": [],
                "Link": [],
                "Summary": [],
                "Address": [],
                "Price": [],
                "Image links": []
                }
        for link in PropertyScraper.get_links():
            im = link[-6:]
            im2 = link[28:35]
            prop_dict["fr-id"].append(im2+im)
            id = uuid.uuid4()
            prop_dict["id"].append(id)
            Scraper.driver.get(link)
            prop_dict["Link"].append(link)
            time.sleep(0.5)
            summary = Scraper.driver.find_element(By.XPATH, '//div[@class="prop-heading-brief"]')
            prop_dict["Summary"].append(summary.text)
            time.sleep(0.5)
            info = Scraper.driver.find_element(By.XPATH, '//div[@class="prop-summary-row"]')
            address = info.find_element(By.XPATH, './/h1')
            prop_dict["Address"].append(address.text)
            time.sleep(0.5)
            price = Scraper.driver.find_element(By.XPATH, '//div[@class="prop-price"]')
            prop_dict["Price"].append(price.text)
            img_list = Scraper.driver.find_elements(By.XPATH, '//div[@class="Slideshow-slides SlideshowCarousel"]//img')
            img_links = []

            
            for img in img_list:
                try:
                    link = img.get_attribute('src')
                    img_links.append(link)
                except:
                    print('No src found')
            prop_dict["Image links"].append(img_links)
            df = pd.DataFrame(prop_dict)
            return prop_dict

#GRAB, DOWNLOAD AND STORE IMAGES

#We store the images in a seperate folder

    def download_images(self, my_dict):
        os.mkdir(f"/Users/ryanhughes/Desktop/Aicore/Property-Pal-Pipeline-/Property_Photos/{Postcode}")
        image_directory = os.path.dirname(f"/Users/ryanhughes/Desktop/Aicore/Property-Pal-Pipeline-/Property_Photos/{Postcode}/")
        img_link_ct= -1
        for img_list in my_dict["Image links"]:
            img_link_ct += 1
            img_ct = 0
            for url in img_list:
                try:
                    img_ct += 1
                    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                    with open(f"{image_directory}/{my_dict['fr-id'][img_link_ct]}_{str(img_ct)}.jpg", "wb") as f:
                        with urllib.request.urlopen(req) as r:
                            f.write(r.read())
                except IndexError:
                    pass 

#SAVE THE RAW DATA

#We take our dictionary and save it as a json file in a seperate folder

    def store_data(self, my_dict):
        old_default = JSONEncoder.default

        def new_default(self, obj):
            if isinstance(obj, UUID):
                return str(obj)
            return old_default(self, obj)

        JSONEncoder.default = new_default
    
        with open(f'/Users/ryanhughes/Desktop/Aicore/Property-Pal-Pipeline-/raw_data/{Postcode}.json', 'w') as f:
            json.dump(my_dict, f, indent = 4)

        df = pd.DataFrame(my_dict)
        return df

if __name__ == "__main__":
    PropertyScraper.login(Scraper)
    PropertyScraper.get_links(Scraper)
    PropertyScraper.get_info(Scraper, PropertyScraper.get_links())
    PropertyScraper.download_images(Scraper, PropertyScraper.get_info())
    PropertyScraper.store_data(Scraper, PropertyScraper.get_info())
