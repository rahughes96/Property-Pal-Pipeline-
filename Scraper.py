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
Postcode = "BT1"

#DEFINE CLASS AND FUNCTIONS

class Scraper:
    def __init__(self, url: str = 'https://www.propertypal.com') -> None:
        self.driver = Chrome(ChromeDriverManager().install())
        self.driver.get(url)
        
    def accept_cookies(self, xpath:str = '//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]'):

        """

        This function accepts the cookies prompt

        Attributes:
            xpath (str): the xpath of the "accept cookies" button
        
        """
        
        try:
            time.sleep(1)
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))

            button = self.driver.find_element(By.XPATH, xpath)
            button.click()
        except TimeoutException:
            print("No Cookies Found")

    
    def search_word(self, xpath, pc = Postcode):

        """

        This function types the desired text into the search bar

        Attributes:
            xpath (str): the xpath of the search bar
            pc (str): the postcode of the desired location (the text typed)

        
        """

        search = self.driver.find_element(By.XPATH, xpath)
        self.driver.implicitly_wait(10)
        ActionChains(self.driver).move_to_element(search).click(search).perform()
        ActionChains(self.driver).send_keys(pc).perform() 
    
    def search_rent(self):

        """
        
        This function clicks the "Rent" search button
        
        """

        rent = self.driver.find_element_by_xpath('//*[@id="searchForm"]/div/div[2]/button[2]')
        rent.click()

    def search_sale(self):

        """
        
        This function clicks the "Sale" search button
        
        """

        sale = self.driver.find_element_by_xpath('//*[@id="searchForm"]/div/div[2]/button[1]')
        sale.click()

    def button_click(self,xpath):

        """

        This function clicks an arbitrary button with a given xpath
        
        Attributes:
            xpath(str): The xpath of the button to be clicked

        """

        button = self.driver.find_element_by_xpath(xpath)
        button.click()
    
    def find_container(self, xpath: str = '//*[@id="body"]/div[3]/div/div[1]/div/ul'):

        """
        
        This function finds and returns a desired container

        Attributes:
            xpath(str): The xpath of the desired container

        """

        self.container = self.driver.find_element(By.XPATH, xpath)
        return self.container