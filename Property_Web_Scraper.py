import time
import uuid
import os
import urllib
import json
import logging
import requests
import sqlalchemy
import boto3
import pandas as pd
from botocore.exceptions import ClientError
from pathlib import Path
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from multiprocessing.sharedctypes import Value
from json import JSONEncoder
from uuid import UUID
from utils.Scraper import Scraper

# NAVIGATE THE WEBSITE

#This block uses a dummy email to log into the website, which avoids problems further down the line

class PropertyScraper(Scraper):

    def __init__(self, url: str = 'https://www.propertypal.com', Headless: bool = True):
        super().__init__(url, Headless)

    def which_postcode(self):
        Postcode = input("Please enter the postcode you would like to scrape:")
        return Postcode

    def login(self, Postcode, Username, Password):

        """

        This function logs in to the given URL and accepts the cookies prompt

        Attributes:
            Postcode (str): The postcode we are going to scrape
            Username (str): The username we need to login (email address) 
            Password (str): password used to login

        """

        self.scraper.button_click('//p[@class="sc-11tz8h0-4 bplBgY"]')
        time.sleep(0.5)
        self.scraper.button_click('//a[@data-testid="loginLink"]')
        time.sleep(0.5)
        self.scraper.search_word('//input[@placeholder="Email address"]',Username)
        self.scraper.search_word('//input[@placeholder="Password"]',Password)
        enter_button = self.scraper.driver.find_element_by_xpath('//*[@id="tabs--1--panel--0"]/div/div[2]/form/div[3]/button')
        enter_button.click()
        time.sleep(2)
        logo = self.scraper.driver.find_element_by_xpath('//*[@id="__next"]/div[1]/nav[1]/a')
        logo.click() 
        self.scraper.search_word('//input[@type="search"]', Postcode)
        time.sleep(2)
        rent_button = self.scraper.driver.find_element_by_xpath('//button[@data-testid="forRentButton"]')
        rent_button.click()
        time.sleep(0.5)

    

#CREATE THE LIST OF LINKS

#We first find the container with which the links for each page are located, in the form of href
    def get_property_links(self):

        """

        This function grabs all the links from each property and stores them in a list

        
        """

        property_links = []
        print("Finding elements...")
        while True:
            time.sleep(2)
            container = self.scraper.find_container()
            
            items = container.find_elements(By.XPATH, './li')

            for element in items:
                try:
                    link = element.find_element(By.XPATH, './/a').get_attribute('href')
                    
                    property_links.append(link)
                except:
                    print("no href found")
            
            try:
                self.scraper.button_click('//a[@aria-label="next page"]')
            except NoSuchElementException:
                print("end of list")
                break
        property_links = list(set(property_links))
        return property_links

#GRAB INFO FROM EACH LINK AND STORE

#We now iterate through our list of links, and grab our desired info, and store it into a dictionary.

    def get_property_info(self, property_links):

        """

        This function takes the list of links and grabs all the desired information and stores 
        them in a dictionary

        Attributes:
            list_links (list): list of all the property links  
        
        """
        self._property_links = property_links
        print("Grabbing info...")
        prop_dict = {"fr-id": [],
                "id": [],
                "Link": [],
                "Summary": [],
                "Address": [],
                "Price": [],
                "Image links": []
                }
        for link in property_links:
            id_pt_1 = link[-6:]
            id_pt_2 = link[28:35]
            prop_dict["fr-id"].append(id_pt_1+id_pt_2)
            id = uuid.uuid4()
            prop_dict["id"].append(id)
            self.scraper.driver.get(link)
            prop_dict["Link"].append(link)
            time.sleep(0.5)
            summary = self.scraper.driver.find_element(By.XPATH, '//p[@class="sc-11tz8h0-4 FViVo"]')
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
            
        return prop_dict

#GRAB, DOWNLOAD AND STORE IMAGES

#We store the images in a seperate folder

    def download_images(self, my_dict, Postcode, Bucket_name):
        """

        This function takes the dictionary and slices out the photo links from it, downloads
        the images and stores them in a seperate file.

        Attributes:
            my_dict (dict): Dictionary of all the information scraped from our given website.
            Postcode (str): The postcode we are going to scrape
        
        """

        self._my_dict = my_dict
        try:
            os.mkdir(f"/Users/ryanhughes/Desktop/Aicore/Proppal/Property-Pal-Pipeline-/Property_Photos/{Postcode}")
        except FileExistsError:
            pass

        image_directory = os.path.dirname(f"/Users/ryanhughes/Desktop/Aicore/Proppal/Property-Pal-Pipeline-/Property_Photos/{Postcode}/")
        img_link_ct= -1
        for img_list in my_dict["Image links"]:
            img_link_ct += 1
            img_ct = 0
            for url in img_list:
                image_name = f"{image_directory}/{my_dict['fr-id'][img_link_ct]}_{str(img_ct)}.jpg"
                image_path = Path(image_name)

#Check if the image file already exists before redownloading it

                if image_path.is_file() == False:

                    try:
                        img_ct += 1
                        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                        with open(image_name, "wb") as f:
                            with urllib.request.urlopen(req) as r:
                                f.write(r.read())

#Upload the file to S3
        
                        r = requests.get(url, stream=True)
                        session = boto3.Session()
                        s3 = session.resource('s3')
                        bucket = s3.Bucket(Bucket_name)
                        folder_name = f"{Postcode}_images"
                        bucket.upload_fileobj(r.raw, f"{folder_name}/{my_dict['fr-id'][img_link_ct]}_{str(img_ct)}")


                    except IndexError:
                        pass 
                else:
                    pass

#SAVE THE RAW DATA

#We take our dictionary and save it as a json file in a seperate folder

    def store_data_locally(self, my_dict, Postcode):
        """

        This function takes the dictionary and stores the information in a json file

        Attributes:
            my_dict (dict): Dictionary of all the information scraped from our given website.
            Postcode (str): The postcode we are going to scrape
        
        """
        self._my_dict = my_dict

        old_default = JSONEncoder.default

        def new_default(self, obj):

            if isinstance(obj, UUID):
                return str(obj)
            return old_default(self, obj)
        JSONEncoder.default = new_default

        with open(f'/Users/ryanhughes/Desktop/Aicore/Proppal/Property-Pal-Pipeline-/raw_data/{Postcode}.json', 'w') as f:json.dump(my_dict, f, indent = 4)
        file_name = (f"/Users/ryanhughes/Desktop/Aicore/Proppal/Property-Pal-Pipeline-/raw_data/{Postcode}.json")
        return file_name


    def upload_file_to_S3(self, file_location, bucket, object_name = None):

        """

        This function uploads the data to an S3 bucket on AWS

        Attributes:
            file_location (str): String describing the path to the file
            Bucket (str): name of the S3 bucket were storing into
            object_name (str): name of the object that wil appear in S3
        
        """

        if object_name is None:
            object_name = os.path.basename(file_location)
        
        s3 = boto3.client('s3')
        try:
            with open(file_location, "rb") as f:
                s3.upload_fileobj(f, bucket, object_name)
        except ClientError as e:
            logging.error(e)
            return False
        return True

    def upload_to_RDS(self, new_dataframe, objectname, Password, Host, Port):
        """

        This function takes the dataframe already scraped previously, compares it to the new dataframe and uploads any new entries to the 
        a relational database

        Attributes:
            old_dataframe (pandas.core.frame.DataFrame): Dataframe of all the properties in that postcode already scraped
            object_name (str): name of the object that wil appear in RDS
            Password (str): password of the RDS
            Host (str): Host of the RDS
            Port(str): Port of the RDS
        
        """
        print("connecting to database...")
        
        engine = sqlalchemy.create_engine(f"postgresql://postgres:{Password}@{Host}:{Port}")

#Take the old dataframe from SQL table and use pandas to check if any of the records already exist
#drop the duplicates and reupload the new dataframe

        try:
            old_dataframe = pd.read_sql_table(objectname, engine)

            merged_dfs = pd.concat([old_dataframe, new_dataframe])
            merged_dfs = merged_dfs.drop_duplicates(subset=["fr-id"], keep=False)

            merged_dfs.to_sql(objectname, engine, if_exists = "append", index=False)

        except ValueError:
            new_dataframe.to_sql(objectname, engine, if_exists = "fail", index=False)
