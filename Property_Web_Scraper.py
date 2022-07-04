import selenium
from selenium import webdriver
from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

class Scraper:
    def __init__(self, url) -> None:
        self.driver = Chrome(ChromeDriverManager().install())
        self.driver.get(url)
        
    def accept_cookies(self, xpath):

        button = self.driver.find_element_by_xpath(xpath)
        button.click()
    
    def search_word(self, xpath, text):

        search_bar = self.driver.find_element_by_xpath(xpath)
        search_bar.click()
        search_bar.send_keys(text)

    def scroll_down(self):
        
        self.driver.execute_script("window.scrollTo(0, 540)") 