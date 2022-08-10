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

    def test_get_links(self):
        self.bot.driver.get("https://www.propertypal.com/property-to-rent/bt3")
        expected_prop_ct = int(self.bot.driver.find_element(By.XPATH, '//strong[@class="f-red"]').text)
        list_links = []
        while True:
            container = self.bot.driver.find_element(By.XPATH, '//*[@id="body"]/div[3]/div/div[1]/div/ul')
            items = container.find_elements(By.XPATH, './li')
            for i in items:
                try:
                    house = i.find_element(By.XPATH, './/a[2]')
                    link = house.get_attribute('href')
                    list_links.append(link)
                except:
                    print("no href found")
            
            try:
                self.bot.button_click('//a[@class="btn paging-next"]')
            except NoSuchElementException:
                print("end of list")
                break
        message = "List of links does not match the number of properties"
        self.assertEqual(expected_prop_ct, len(list_links), message)

    def teardown(self):
        pass

if __name__ == "__main__":
    unittest.main() 
