import unittest
import Property_Web_Scraper
import time
import Scraper
from Property_Web_Scraper import PropertyScraper
from selenium.webdriver.common.by import By

class TestScraper(unittest.TestCase):
    def setUp(self):
        self.bot = Property_Web_Scraper.Scraper()

    def test_accept_cookies(self):
        self.bot.accept_cookies()
        
        self.bot.driver.find_element(By.XPATH, '//a[@class="mainnav-logo"]')

    def test_login(self):
        self.bot.button_click('//a[@href="/login"]')
        self.bot.search_word('//input[@placeholder="Email address"]','sopranotony233@gmail.com')
        self.bot.search_word('//input[@placeholder="Password"]','sopranotony321')
        enter_button = self.bot.driver.find_element_by_xpath('//*[@id="root"]/div/div/div/div/div/div[1]/div/div[2]/div[2]/form/button')
        enter_button.click()
        time.sleep(2)
        logo = self.bot.driver.find_element_by_xpath('//a[@class="mainnav-logo"]')
        logo.click() 
        self.bot.search_word('//*[@id="searchForm"]/div/div[1]')
        time.sleep(2)
        rent_button = self.bot.driver.find_element_by_xpath('//*[@id="searchForm"]/div/div[2]/button[2]')
        rent_button.click()
        self.bot.driver.find_element(By.XPATH, '//div[@class="maxwidth"]')

    def teardown(self):
        pass

if __name__ == "__main__":
    unittest.main() 