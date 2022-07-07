# Property-Pal-Pipeline-
AiCore project 2

**Milestone 1**
The webpage I chose to scrape is PropertyPal.com, a platform to view local properties for sale and rent. By using the selenium package and Webdriver, PropertyPal has a vast quantity of retrievable data. Every property has a host of information we can scrape including location, size, No. of bedrooms etc. Having recently moved home this seemed like an enjoyable way to build my first data pipeline.

**Milestone 2**
-Task 1

Before starting to build the scraper, some modules need to be imported. These were added to as and when needed.

<img width="521" alt="Screenshot 2022-07-07 at 11 11 30" src="https://user-images.githubusercontent.com/102994234/177749717-1e4e6caf-8723-43f0-a87e-e89a0fcbe277.png">

For the initial build of the scraper class I planned on using, I created a class and called it "Scraper" using object oriented programming. I then built some very simple methods in it that I could use to navigate any website, clicking buttons and scrolling etc. 

Inside the new Scraper class, it took one argument, which was set by default to the URL of said webpage. Using the "get" method, the webpage is loaded in a Chrome browser.

Now that that the beginings of the class have been built, an instance of the class can be initialised.



