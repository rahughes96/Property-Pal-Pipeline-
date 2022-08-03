import unittest
import Property_Web_Scraper
from selenium.webdriver.common.by import By

class TestScraper(unittest.TestCase):
    def setUp(self):
        self.bot = Property_Web_Scraper.Scraper()

    def test_accept_cookies(self):
        self.bot.accept_cookies()
        
        self.bot.driver.find_element(By.XPATH, '//a[@class="mainnav-logo"]')

    def test_search_word(self):
        self.bot.search_word("")

    def teardown(self):
        pass

if __name__ == "__main__":
    unittest.main()