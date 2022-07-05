import selenium
from selenium import webdriver
from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time


class Scraper:
    def __init__(self, url: str = 'https://www.propertypal.com') -> None:
        self.driver = Chrome(ChromeDriverManager().install())
        self.driver.get(url)
        
    def ivan_accept_cookies(self, xpath):

        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(By.XPATH, xpath))

            button = self.driver.find_element(By.XPATH, xpath)
            button.click()
        except TimeoutException:
            print("No Cookies Found")

    def accept_cookies(self, xpath:str = '//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]'):
        button = self.driver.find_element(By.XPATH, xpath)
        button.click()

    
    def search_word(self, xpath, text):

        search = self.driver.find_element(By.XPATH, xpath)
        self.driver.implicitly_wait(10)
        ActionChains(self.driver).move_to_element(search).click(search).perform()
        ActionChains(self.driver).send_keys(text).perform()

    def scroll_down(self):
        
        self.driver.execute_script("window.scrollTo(0, 540)") 
    
    def search_rent(self):
        rent = self.driver.find_element_by_xpath('//*[@id="searchForm"]/div/div[2]/button[2]')
        rent.click()

    def search_sale(self):
        rent = self.driver.find_element_by_xpath('//*[@id="searchForm"]/div/div[2]/button[1]')
        rent.click()

if __name__ == "__main__":
    bot = Scraper()
    bot.accept_cookies()
    time.sleep(3)
    bot.search_word('//*[@id="searchForm"]/div/div[1]', 'bt4')
    time.sleep(3)
    bot.search_rent()