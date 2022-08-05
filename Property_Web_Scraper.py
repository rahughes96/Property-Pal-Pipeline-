import time
import uuid
import os
import urllib
import json
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from json import JSONEncoder
from uuid import UUID
from Scraper import Scraper

global Postcode
Postcode = "BT1"

# NAVIGATE THE WEBSITE

#This block uses a dummy email to log into the website, which avoids problems further down the line

class PropertyScraper(Scraper):

    def __init__(self, url: str = 'https://www.propertypal.com'):
        self.scraper = Scraper() 

    def login(self):
        self.scraper.button_click('//a[@href="/login"]')
        self.scraper.search_word('//input[@placeholder="Email address"]','sopranotony233@gmail.com')
        self.scraper.search_word('//input[@placeholder="Password"]','sopranotony321')
        enter_button = self.scraper.driver.find_element_by_xpath('//*[@id="root"]/div/div/div/div/div/div[1]/div/div[2]/div[2]/form/button')
        enter_button.click()
        time.sleep(2)
        logo = self.scraper.driver.find_element_by_xpath('//a[@class="mainnav-logo"]')
        logo.click() 
        self.scraper.search_word('//*[@id="searchForm"]/div/div[1]')
        time.sleep(2)
        rent_button = self.scraper.driver.find_element_by_xpath('//*[@id="searchForm"]/div/div[2]/button[2]')
        rent_button.click()
        time.sleep(2)

    

#CREATE THE LIST OF LINKS

#We first find the container with which the links for each page are located, in the form of href
    def get_links(self):
        list_links = []
        print("Finding elements...")
        while True:
            container = self.scraper.find_container()
            items = container.find_elements(By.XPATH, './li')
            for i in items:
                try:
                    house = i.find_element(By.XPATH, './/a[2]')
                    link = house.get_attribute('href')
                    list_links.append(link)
                except:
                    print("no href found")
            
            try:
                self.scraper.button_click('//a[@class="btn paging-next"]')
            except NoSuchElementException:
                print("end of list")
                break
        return list_links

#GRAB INFO FROM EACH LINK AND STORE

#We now iterate through our list of links, and grab our desired info, and store it into a dictionary.

    def get_info(self, list_links):
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
            id_pt_1 = link[-6:]
            id_pt_2 = link[28:35]
            prop_dict["fr-id"].append(id_pt_1+id_pt_2)
            id = uuid.uuid4()
            prop_dict["id"].append(id)
            self.scraper.driver.get(link)
            prop_dict["Link"].append(link)
            time.sleep(0.5)
            summary = self.scraper.driver.find_element(By.XPATH, '//div[@class="prop-heading-brief"]')
            prop_dict["Summary"].append(summary.text)
            time.sleep(0.5)
            info = self.scraper.driver.find_element(By.XPATH, '//div[@class="prop-summary-row"]')
            address = info.find_element(By.XPATH, './/h1')
            prop_dict["Address"].append(address.text)
            time.sleep(0.5)
            price = self.scraper.driver.find_element(By.XPATH, '//div[@class="prop-price"]')
            prop_dict["Price"].append(price.text)
            img_list = self.scraper.driver.find_elements(By.XPATH, '//div[@class="Slideshow-slides SlideshowCarousel"]//img')
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

        with open(f'/Users/ryanhughes/Desktop/Aicore/Property-Pal-Pipeline-/raw_data/{Postcode}.json', 'w') as f:json.dump(my_dict, f, indent = 4)
        df = pd.DataFrame(my_dict)
        return df

if __name__ == "__main__":
    print("lets go")
    bot = PropertyScraper()
    print('starting..')
    bot.login()
    print('log in?')
    list_links = bot.get_links()
    print(list_links)
    print(len(list_links))
    print("links attained?")
    my_dict = bot.get_info(list_links)
    print("info Attained?")
    bot.download_images(my_dict)
    print("images downloaded?")
    bot.store_data(my_dict)
    print("data Stored?")
    print("finished")
