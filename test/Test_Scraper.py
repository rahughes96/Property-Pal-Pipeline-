import unittest
import Property_Web_Scraper
import time
import Scraper
from selenium.common.exceptions import NoSuchElementException
from Property_Web_Scraper import PropertyScraper
from selenium.webdriver.common.by import By

class TestScraper(unittest.TestCase):
    def setUp(self):
        self.bot = Property_Web_Scraper.Scraper()

    def test_accept_cookies(self):
        self.bot.accept_cookies()
        
        self.bot.driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/nav[1]/a')

    def test_login(self, Postcode = "bt1"):
        self.bot.button_click('//*[@id="__next"]/div[1]/nav[1]/li/button')
        time.sleep(0.5)
        self.bot.button_click('//*[@id="__next"]/div[1]/nav[1]/li/ul/li[1]/a')
        time.sleep(0.5)
        self.bot.search_word('//input[@placeholder="Email address"]','sopranotony233@gmail.com')
        self.bot.search_word('//input[@placeholder="Password"]','sopranotony321')
        enter_button = self.bot.driver.find_element_by_xpath('//*[@id="tabs--1--panel--0"]/div/div[2]/form/div[3]/button')
        enter_button.click()
        time.sleep(2)
        logo = self.bot.driver.find_element_by_xpath('//*[@id="__next"]/div[1]/nav[1]/a')
        logo.click() 
        self.bot.search_word('//input[@data-testid="searchInput"]', Postcode)
        time.sleep(2)
        rent_button = self.bot.driver.find_element_by_xpath('//button[@data-testid="forSaleButton"]')
        rent_button.click()
        time.sleep(0.5)
        self.bot.driver.find_element(By.XPATH, '//button[@data-testid="saveThisSearch"]')

    def test_get_links(self):
        self.bot.driver.get("https://www.propertypal.com/property-to-rent/bt3")
        self.bot.accept_cookies()
        time.sleep(2)
        expected_prop_ct = int(self.bot.driver.find_element(By.XPATH, '//strong[@class="typography__Bold-sc-11tz8h0-9 gCJJgH"]').text)
        list_links = []
        print("Finding elements...")
        while True:
            time.sleep(2)
            container = self.bot.find_container()
            items = container.find_elements(By.XPATH, './li')
            for i in items:
                try:
                    house = i.find_element(By.XPATH, './/a')
                    link = house.get_attribute('href')
                    list_links.append(link)
                except:
                    print("no href found")
            
            try:
                self.bot.button_click('//a[@aria-label="next page"]')
            except NoSuchElementException:
                print("end of list")
                break
        message = "List of links does not match the number of properties"
        self.assertEqual(expected_prop_ct, len(list_links), message)

    def teardown(self):
        pass

if __name__ == "__main__":
    unittest.main() 
