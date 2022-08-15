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
Postcode = input("Please enter the postcode you would like to scrape:")

# NAVIGATE THE WEBSITE

#This block uses a dummy email to log into the website, which avoids problems further down the line

class PropertyScraper(Scraper):

    def __init__(self, url: str = 'https://www.propertypal.com'):
        self.scraper = Scraper() 

    def login(self):

        """

        This function logs in to the given URL and accepts the cookies prompt

        
        """

        self.scraper.button_click('//*[@id="__next"]/div[1]/nav[1]/li/button')
        time.sleep(0.5)
        self.scraper.button_click('//*[@id="__next"]/div[1]/nav[1]/li/ul/li[1]/a')
        time.sleep(0.5)
        self.scraper.search_word('//input[@placeholder="Email address"]','sopranotony233@gmail.com')
        self.scraper.search_word('//input[@placeholder="Password"]','sopranotony321')
        enter_button = self.scraper.driver.find_element_by_xpath('//*[@id="tabs--1--panel--0"]/div/div[2]/form/div[3]/button')
        enter_button.click()
        time.sleep(2)
        logo = self.scraper.driver.find_element_by_xpath('//*[@id="__next"]/div[1]/nav[1]/a')
        logo.click() 
        self.scraper.search_word('//*[@id="main"]/div[1]/div/div[15]/form/div[1]/input', Postcode)
        time.sleep(2)
        rent_button = self.scraper.driver.find_element_by_xpath('//*[@id="main"]/div[1]/div/div[15]/form/div[2]/button[2]')
        rent_button.click()
        time.sleep(0.5)

    

#CREATE THE LIST OF LINKS

#We first find the container with which the links for each page are located, in the form of href
    def get_links(self):

        """

        This function grabs all the links from each property and stores them in a list

        
        """

        list_links = []
        print("Finding elements...")
        while True:
            container = self.scraper.find_container()
            items = container.find_elements(By.XPATH, './li')
            for i in items:
                try:
                    house = i.find_element(By.XPATH, './/a')
                    link = house.get_attribute('href')
                    list_links.append(link)
                except:
                    print("no href found")
            
            try:
                self.scraper.button_click('//a[@aria-label="next page"]')
            except NoSuchElementException:
                print("end of list")
                break
        return list_links

#GRAB INFO FROM EACH LINK AND STORE

#We now iterate through our list of links, and grab our desired info, and store it into a dictionary.

    def get_info(self, list_links):

        """

        This function takes the list of links and grabs all the desired information and stores 
        them in a dictionary

        Attributes:
            list_links (list): list of all the property links  
        
        """
        self._list_links = list_links
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
            summary = self.scraper.driver.find_element(By.XPATH, '//p[@class="typography__Text-sc-11tz8h0-4 ghGziD"]')
            prop_dict["Summary"].append(summary.text)
            time.sleep(0.5)
            address = self.scraper.driver.find_element(By.XPATH, '//*[@id="main"]/div[2]/div[2]/div[2]/div/div[1]/div[1]/h1')
            prop_dict["Address"].append(address.text)
            time.sleep(0.5)
            price = self.scraper.driver.find_element(By.XPATH, '//*[@id="main"]/div[2]/div[2]/div[2]/div/div[1]/div[1]/p[3]/span/strong')
            prop_dict["Price"].append(price.text)
            img_list = self.scraper.driver.find_elements(By.XPATH, '//div[@class="swiper-wrapper"]//img[1]')
            img_links = []

            
            for img in img_list:
                try:
                    link = img.get_attribute('src')
                    img_links.append(link)
                except:
                    print('No src found')
            img_links = list(set(img_links))
            prop_dict["Image links"].append(img_links)
            df = pd.DataFrame(prop_dict)
        return prop_dict

#GRAB, DOWNLOAD AND STORE IMAGES

#We store the images in a seperate folder

    def download_images(self, my_dict):
        """

        This function takes the dictionary and slices out the photo links from it, downloads
        the images and stores them in a seperate file.

        Attributes:
            my_dict (dict): Dictionary of all the information scraped from our given website.
        
        """

        self._my_dict = my_dict
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
        """

        This function takes the dictionary and stores the information in a json file

        Attributes:
            my_dict (dict): Dictionary of all the information scraped from our given website.
        
        """
        self._my_dict = my_dict

        old_default = JSONEncoder.default

        def new_default(self, obj):

            if isinstance(obj, UUID):
                return str(obj)
            return old_default(self, obj)
        JSONEncoder.default = new_default

        with open(f'/Users/ryanhughes/Desktop/Aicore/Property-Pal-Pipeline-/raw_data/{Postcode}.json', 'w') as f:json.dump(my_dict, f, indent = 4)
        df = pd.DataFrame(my_dict)
        return df


