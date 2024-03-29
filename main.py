import pandas as pd
import json
from utils.Property_Web_Scraper import PropertyScraper

if __name__ == "__main__":

# Establish and assign your credentials 

    with open('credentials.json') as cred:
        credentials = json.load(cred)
    RDS_HOST = credentials['RDS_HOST']
    RDS_PASSWORD = credentials['RDS_PASSWORD']
    RDS_PORT = credentials['RDS_PORT']
    Property_Pal_Username = credentials["PROPERTY_PAL_USERNAME"]
    Property_Pal_Password = credentials["PROPERTY_PAL_PASSWORD"]
    Bucket_name = credentials["Bucket_Name"]

#Start up the scraper, login and begin grabbing your desired info

    print("lets go")
    bot = PropertyScraper()
    Postcode = bot.which_postcode()
    print('starting...')
    bot.login(Postcode, Property_Pal_Username, Property_Pal_Password)
    print('logging in...')
    list_property_links = bot.get_property_links()
    print("links attained")
    list_links_length = len(list_property_links)
    print(f"list links = {list_links_length}")

    #Assign all the info into a dataframe

    property_dict = bot.get_property_info(list_property_links)
    dataframe = pd.DataFrame.from_dict(property_dict)
    print("info Attained")

    print("downloading images...")
    bot.download_images(property_dict, Postcode, Bucket_name)
    print("images downloaded")
    file_name = (f"/Users/ryanhughes/Desktop/Aicore/Proppal/Property-Pal-Pipeline-/raw_data/{Postcode}.json")


    
    while True:
        local_or_RDS = input("Would you like to save data to your local drive, upload to RDS or both? pleae type 'local', 'RDS' or 'both':")
        if local_or_RDS == "local":

            bot.store_data_locally(property_dict, Postcode)
            print("data Stored locally")
            bot.upload_file_to_S3(file_name, Bucket_name, file_name[-8:-5])
            print("data uploaded to S3")
            break

        elif local_or_RDS == "RDS":

            bot.upload_to_RDS(dataframe, file_name[-8:-5], RDS_PASSWORD, RDS_HOST, RDS_PORT)
            print("data uploaded to RDS")
            break

        elif local_or_RDS == "both":
            bot.store_data_locally(property_dict, Postcode)
            print("Data stored locally")
            bot.upload_file_to_S3(file_name, Bucket_name, file_name[-8:-5]) 

            bot.upload_to_RDS(dataframe, file_name[-8:-5], RDS_PASSWORD, RDS_HOST, RDS_PORT)
            print("Data uploaded to RDS")
            break           

        else:
            print("Im sorry, I didnt understand :S")
    

        
    print("finished")
    print("have a great day!")
    
