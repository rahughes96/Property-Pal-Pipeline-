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
        
    def ivan_accept_cookies(self, xpath:str = '//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]'):
        
        try:
            time.sleep(1)
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))

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

    def button_click(self,xpath):
        button = self.driver.find_element_by_xpath(xpath)
        button.click()
    
    def find_container(self, xpath: str = '//*[@id="body"]/div[3]/div/div[1]/div/ul'):
        self.container = self.driver.find_element(By.XPATH, xpath)
        return self.container

if __name__ == "__main__":
    bot = Scraper()
    bot.ivan_accept_cookies()
    time.sleep(2)
    bot.button_click('//a[@href="/login"]')
    time.sleep(2)
    bot.search_word('//input[@placeholder="Email address"]','sopranotony233@gmail.com')
    time.sleep(2)
    bot.search_word('//input[@placeholder="Password"]','sopranotony321')
    time.sleep(2)
    bot.button_click('//*[@id="root"]/div/div/div/div/div/div[1]/div/div[2]/div[2]/form/button')
    time.sleep(2)
    bot.button_click('//a[@class="mainnav-logo"]')  
    time.sleep(2)
    bot.search_word('//*[@id="searchForm"]/div/div[1]', 'bt4')
    time.sleep(2)
    bot.search_rent()
    time.sleep(2)
    print("Finding container")
    container = bot.find_container()
    print("Finding elements")
    items = container.find_elements(By.XPATH, './li')
    list_links = []

    for i in items:
        try:
            house = i.find_element(By.XPATH, './/a[2]')
            link = house.get_attribute('href')
            list_links.append(link)
        except:
            print('No href found, skipping this property')
    print(list_links)
    prop_dict = {"Link": [],
             "Summary": [],
            "Address": []
            }
    for link in list_links:
        bot.driver.get(link)
        prop_dict["Link"].append(link)
        time.sleep(1)
        summary = bot.driver.find_element(By.XPATH, '//div[@class="prop-heading-brief"]')
        prop_dict["Summary"].append(summary.text)
        time.sleep(1)
        info = bot.driver.find_element(By.XPATH, '//div[@class="prop-summary-row"]')
        address = info.find_element(By.XPATH, './/h1')
        prop_dict["Address"].append(address.text)
        time.sleep(1)
        
    print(prop_dict)