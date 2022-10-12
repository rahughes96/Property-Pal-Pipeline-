import time
from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

global Postcode

#DEFINE CLASS AND FUNCTIONS

class Scraper:
    def __init__(self, url: str = 'https://www.propertypal.com', accept_cookies_xpath: str = '//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]'):
        """

        This function logs in to the given URL and accepts the cookies prompt

        Attributes:
            url (str): The url of given website 
            xpath (str): The xpath of the "accept cookies" button
        
        """
        
        self.driver = Chrome(ChromeDriverManager().install())
        self.driver.get(url)
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, accept_cookies_xpath)))

            button = self.driver.find_element(By.XPATH, accept_cookies_xpath)
            button.click()
        except TimeoutException:
            print("No Cookies Found")


    
    def search_word(self, xpath, pc):

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
        
    def accept_cookies(self, xpath:str = '//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]'):

        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))

            button = self.driver.find_element(By.XPATH, xpath)
            button.click()
        except TimeoutException:
            print("No Cookies Found")

    def button_click(self, xpath):

        """

        This function clicks an arbitrary button with a given xpath
        
        Attributes:
            xpath(str): The xpath of the button to be clicked

        """

        button = self.driver.find_element_by_xpath(xpath)
        button.click()
    
    def find_container(self, xpath: str = '//ul[@class="sc-1rcidgz-0 jYKFvf"]'):

        """
        
        This function finds and returns a desired container

        Attributes:
            xpath(str): The xpath of the desired container

        """

        container = self.driver.find_element(By.XPATH, xpath)
        return container