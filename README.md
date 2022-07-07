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

_Task 4_

In order to eventually get the links to the pages where the required details can be found, a few more methods were added to the Scraper class. The first one being the search bar.

Initially tried another simple button.click() from selenium, however it required a sturdier method to find and click the button, and send keys. I found ActionChains, a more advanced version of the actions you can do with selenium, to work. This paired with seleniums ImplicitlyWait method allowed for the search bar to be found and typed into.

<img width="726" alt="Screenshot 2022-07-07 at 11 44 32" src="https://user-images.githubusercontent.com/102994234/177755671-5a135c3e-15a5-43b2-a83e-8afd5f2a9006.png">

Instead of a normal search bar, PropertyPal has either "Rent" or "Buy" as its search buttons, so a method was created to click both, although we will most likely focus on just rentals.

<img width="714" alt="Screenshot 2022-07-07 at 11 55 32" src="https://user-images.githubusercontent.com/102994234/177757556-3889aa04-5a75-47f1-bf20-ff6aee6c3f53.png">

In order to find the container with all the information required, we need to examine the html code of the website. I found that all the links were inside a "ul" and each were in the daughter tags "li".

<img width="289" alt="Screenshot 2022-07-07 at 11 59 57" src="https://user-images.githubusercontent.com/102994234/177758312-7566ce0e-f763-4735-a971-2940c4cc7c18.png">

I used the following method, with the default argument as the xpath for the said "ul" tag, in order to store our container.

<img width="612" alt="Screenshot 2022-07-07 at 12 01 51" src="https://user-images.githubusercontent.com/102994234/177758616-3b1cec59-0448-48ef-8e6b-46571bcc0486.png">

Once the container was found, an empty list was created, then using a "for" loop, the container was iterated through to grab the "a" tag and then extract the "href" which we can see in the html code, lies the links we require.

<img width="403" alt="Screenshot 2022-07-07 at 13 32 24" src="https://user-images.githubusercontent.com/102994234/177774099-c04f8ea1-7b51-4492-8b14-3cc5428494b0.png">

Then for each link, we appended this to our empty list, resulting in a list of all the links we needed for that page.

<img width="480" alt="Screenshot 2022-07-07 at 13 33 15" src="https://user-images.githubusercontent.com/102994234/177774198-61ec20d6-dbaf-4381-b284-8909dd361402.png">

_Task 5_

By running the entire body of code through an "if __name__ == __main__" statement, we prevent the code from automatically running if we want to iherit any of the methods we use in our Scraper class in a different file. The final block of code for our scraper looks as follows.

<img width="745" alt="Screenshot 2022-07-07 at 13 37 46" src="https://user-images.githubusercontent.com/102994234/177775126-1430491b-0063-4916-8293-0ecf87fd9d44.png">

This opens the webpage, accepts the cookies, searches "BT4" in the rentals category, then grabs all the links from all the properties shown on that page and stores them in the list "list_links".

