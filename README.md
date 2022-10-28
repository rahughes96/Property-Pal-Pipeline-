# Property-Pal-Pipeline-
AiCore project 2

**Milestone 1 - Set Up the Enviroment**

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

Once the container was found, an empty list was created, then, using a "for" loop, the container was iterated through to grab the "a" tag and then extract the "href" which we can see in the html code, lies the links we require.

<img width="403" alt="Screenshot 2022-07-07 at 13 32 24" src="https://user-images.githubusercontent.com/102994234/177774099-c04f8ea1-7b51-4492-8b14-3cc5428494b0.png">

Then for each link, we appended this to our empty list, resulting in a list of all the links we needed for that page.

<img width="519" alt="Screenshot 2022-07-09 at 10 54 42" src="https://user-images.githubusercontent.com/102994234/178100827-f97a0415-7288-4850-80c9-8ad45f4b46f6.png">

_Task 5_

By running the entire body of code through an "if __name__ == __main__" statement, we prevent the code from automatically running if we want to iherit any of the methods we use in our Scraper class in a different file. The final block of code for our scraper looks as follows.

<img width="745" alt="Screenshot 2022-07-07 at 13 37 46" src="https://user-images.githubusercontent.com/102994234/177775126-1430491b-0063-4916-8293-0ecf87fd9d44.png">

This opens the webpage, accepts the cookies, searches "BT4" in the rentals category, then grabs all the links from all the properties shown on that page and stores them in the list "list_links".


**Milestone 2 - Decide Which Website you are Going to Collect Data From**

The webpage I chose to scrape is PropertyPal.com, a platform to view local properties for sale and rent. By using the selenium package and Webdriver, PropertyPal has a vast quantity of retrievable data. Every property has a host of information we can scrape including location, size, No. of bedrooms etc. Having recently moved home this seemed like an enjoyable way to build my first data pipeline.

**Milestone 3 - Navigate the website and collect data**

_Task 1_

Thw information that seemed the most valueble was the address of each prperty, summary of the property (type, how many bedrooms), the price of the property per month and a few images. Firstly, a dictionary was created, each of the values being empty lists, each of the keys a title.

<img width="228" alt="Screenshot 2022-07-17 at 12 19 20" src="https://user-images.githubusercontent.com/102994234/179395721-1049720d-8f88-4813-8f7b-2d09e6701e7e.png">

The information, excluding the images, could be gathered effectively just using the xpaths in a single stroke. Once the information was located, it was appended to the afformentioned dictionary and wrapped in a for loop iterating through each of the property links.

<img width="607" alt="Screenshot 2022-07-17 at 12 17 00" src="https://user-images.githubusercontent.com/102994234/179395619-bc0d8122-a8e0-4c45-9f26-2fd806abd96d.png">

For the images we needed a step further. In order to get multiple images from each property link, a nested for loop was used, iterating through the a container within the webpage. We wanted to attain the attribute 'src' whihc has the image link.

<img width="708" alt="Screenshot 2022-07-17 at 12 25 09" src="https://user-images.githubusercontent.com/102994234/179395866-821c64e9-4c38-4c48-aa8f-da2076b59f13.png">

_Task 2 & 3_

In order to determine a unique id for each property, we needed to look at the url itself initally, and find a number or sequence that would make it identifiable for a computer, and append it with something that made it easier for us to id it. I used index slicing and the .append() method to achieve this.

<img width="252" alt="Screenshot 2022-07-17 at 12 30 22" src="https://user-images.githubusercontent.com/102994234/179396042-24e9a87f-e6eb-470a-afd5-25d2bddc1a6a.png">

Since the link itself had both the address and a unique id number, it was convenient to grab these and add them together.

To generate a globally unique id, we had to use the uuid package and generate a v4 UUID and attatch it to each property.

<img width="283" alt="Screenshot 2022-07-17 at 12 35 58" src="https://user-images.githubusercontent.com/102994234/179396270-3444ded8-dde1-48c1-a35d-513b58b8c36e.png">

_Task 4_

Now that all the information is gathered and we can properly identify each property, we can append this all to our dictionary with empty lists as values. This is done using a for nested for loop, first loop to gather the text information, second to grab all the images.

<img width="739" alt="Screenshot 2022-07-17 at 12 47 34" src="https://user-images.githubusercontent.com/102994234/179396692-6a72730d-9ed5-4533-8dea-84b2fa0287e9.png">

_Task 5_

Having a dictionary that contains everything is a useful thing, however on the off chance that something goes wrong and the computer crashes or deletes it accidentally, all the valueble information will be lost. To prevent this, we have to save all the raw data in a seperate json file.

<img width="721" alt="Screenshot 2022-07-17 at 12 55 00" src="https://user-images.githubusercontent.com/102994234/179396988-c0883c36-51be-4b3d-8ab8-acb51cc9e060.png">

This however through up an error that reported "uuid is not json serialisable". This was fixed using the following block of code.

<img width="272" alt="Screenshot 2022-07-17 at 12 57 50" src="https://user-images.githubusercontent.com/102994234/179397111-855040bc-a81c-408d-8b61-4229aea26050.png">

_Task 6_

So in our dictionary we have all the info, however we still only have the image links, we want to download and store the images. We first made a directory to save our pictures, and named this "Property_Photos"

<img width="882" alt="Screenshot 2022-07-17 at 13 03 16" src="https://user-images.githubusercontent.com/102994234/179397342-eb7fa8bd-7306-4765-bc09-5574f99607b6.png">

We then looped through each of the image links and downloaded the photos and saved them in a file that corresponds to their postcode, in this case "BT3"

<img width="795" alt="Screenshot 2022-07-17 at 13 04 27" src="https://user-images.githubusercontent.com/102994234/179397392-e136975a-90d8-48f8-acee-62f6d19cab16.png">

img_ct was used to number each image so we could distinguish multiple images for one property. We also needed another nested loop in order to loop through the links for each property, and gather the images for each link. A try and except method meant we werent getting the error message for when the dictionary ran out of links.


**Milestone 4 - Documentation and Testing**

_Task 1 & 2_

Refactoring and optimising code is a constant process throughout the building of the code, This comesin many forms including reducing the number of nested for loops and reducing the big O notaition.

By adding docstrings to Each of my functions, it makes the code more readable and thus more reusable to myself and others if I wish to collaborate.

_Task 3_

For two of my public methods, I tested the code was working by checking that an element, that I knew only appeared if the code was executed properly, was there.

For the get_links method, I wanted to check that I had the correct number of links, so I matched this with the number thats stated on the website itself to the length of the list I had attained.

![Screenshot 2022-08-15 at 12 18 13](https://user-images.githubusercontent.com/102994234/184626079-735af40b-6df0-4974-beb2-5c7009a134a2.png)

_Task 4 & 5_

These testing methods were stored in a file named Test_Scraper.py and ran through a If __name__="__main__" statement.

![Screenshot 2022-08-15 at 12 21 31](https://user-images.githubusercontent.com/102994234/184626483-02a42a8c-2074-4c68-967c-c042ab98e8f3.png)

I then used the "python -m test.Test_Scraper" call in my terminal to run the test and checked that all my tests were passing.

**Milestone 5 - Conatinerise the Scraper**

_Task 1 & 2_

Check all tests are passing, putting a final refactoring on the code before containerising

_Task 3_

in order to run the scraper in headless mode I put it in the __init__ method of the Scraper class as a boolean, like so:

![Screenshot 2022-10-28 at 16 37 56](https://user-images.githubusercontent.com/102994234/198677298-1e1f436b-1980-4976-a724-6d26dd053ae0.png)

This meant that when initialising the Scraper, users can define whether they run it headless or not.

_Task 4_

To Create the Docker image I first had to create a requirements file, that would then be used to install the required packages and libraries.

![Screenshot 2022-10-28 at 16 40 12](https://user-images.githubusercontent.com/102994234/198677794-7fd615c7-eca4-446d-ac90-83e2fd49248a.png)

Then creating the Dockerfile like so:

![Screenshot 2022-10-28 at 16 40 51](https://user-images.githubusercontent.com/102994234/198677937-617dbc1e-bf6c-441b-9ac3-afe581b8eea4.png)

_Task 5_

Then after creating a dockerhub account I pushed the newly made container to dockerhub.

**Milestone 6 - Set up a CI/CD Pipeline for your Image**

_Task 1_

Set up github secrets that contained the dockerhub username as well as one woth te dockerhub access token, generated and retrieved from the my dockerhub account page

_Task 2_

Created a github action, following the instructions on the docker documentation website, that is triffered on a push to the main branch of my repository. This action builds the Docker image and then pushes to my Dockerhub account


