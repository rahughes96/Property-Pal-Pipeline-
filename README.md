# Property-Pal-Pipeline-
AiCore project 2

**Milestone 1**

The webpage I chose to scrape is PropertyPal.com, a platform to view local properties for sale and rent. By using the selenium package and Webdriver, PropertyPal has a vast quantity of retrievable data. Every property has a host of information we can scrape including location, size, No. of bedrooms etc. Having recently moved home this seemed like an enjoyable way to build my first data pipeline.

**Milestone 2**

_Task 1 & 2_

Before starting to build the scraper, some modules need to be imported. These were added to as and when needed.

<img width="521" alt="Screenshot 2022-07-07 at 11 11 30" src="https://user-images.githubusercontent.com/102994234/177749717-1e4e6caf-8723-43f0-a87e-e89a0fcbe277.png">

For the initial build of the scraper class I planned on using, I created a class and called it "Scraper" using object oriented programming. I then built some very simple methods in it that I could use to navigate any website, clicking buttons and scrolling etc. 

Inside the new Scraper class, it took one argument, which was set by default to the URL of said webpage. Using the "get" method, the webpage is loaded in a Chrome browser.

<img width="635" alt="Screenshot 2022-07-07 at 11 14 04" src="https://user-images.githubusercontent.com/102994234/177750213-bc2178c3-2428-4c61-ac90-d31f94e542d9.png">
<img width="600" alt="Screenshot 2022-07-07 at 11 14 26" src="https://user-images.githubusercontent.com/102994234/177750292-66fd7c11-d70f-4316-bc2c-f1354d1d873b.png">
<img width="601" alt="Screenshot 2022-07-07 at 11 14 43" src="https://user-images.githubusercontent.com/102994234/177750325-359908da-9b79-442d-b811-9e093b32affc.png">

Inside the new Scraper class, it took one argument, which was set by default to the URL of said webpage. Using the "get" method, the webpage is loaded in a Chrome browser.

Now that that the beginings of the class have been built, an instance of the class can be initialised. 

<img width="193" alt="Screenshot 2022-07-07 at 11 19 44" src="https://user-images.githubusercontent.com/102994234/177751304-92f73711-caef-4b48-ab56-55af45c2fbb3.png">

This loads the webpage in chrome.

_Task 3_

Accepting cookies is the first hurdle to jump when scraping PropertyPal. Intiially using the time module and using sleep(2), this gave the webdriver enough time to let the webpage load, then finding the "accept cookies" button's xpath, used the driver.click(xpath). However I chose to change to the more robust method of WebDriverWait wih the expected conditions (EC). This way the driver would wait until such an xpath was found, instead of waiting for an explicit amount of time and then looking.

This was wrapped in a "try" and "except" whereby if no "accept cookies" was found it will throw us an error. The method's argument was set to default as the xpath of the given "accept cookies" button.

<img width="749" alt="Screenshot 2022-07-07 at 11 35 28" src="https://user-images.githubusercontent.com/102994234/177754145-c72672c9-2489-4add-80e5-248d72cd1d96.png">







