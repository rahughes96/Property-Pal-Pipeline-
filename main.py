import pandas as pd
from Property_Web_Scraper import PropertyScraper

if __name__ == "__main__":
    print("lets go")
    bot = PropertyScraper()
    Postcode = bot.which_postcode()
    print('starting...')
    bot.login(Postcode)
    print('logging in...')
    list_links = bot.get_links()
    print("links attained")
    list_links_length = len(list_links)
    print(f"list links = {list_links_length}")
    my_dict = bot.get_info(list_links)
    dataframe = pd.DataFrame.from_dict(my_dict)
    print("info Attained")

    bot.download_images(my_dict, Postcode)
    print("images downloaded")
    file_name = (f"/Users/ryanhughes/Desktop/Aicore/Proppal/Property-Pal-Pipeline-/raw_data/{Postcode}.json")
    bot.upload_file_to_S3(file_name, "propertypal", file_name[-8:-5])


    
    while True:
        local_or_S3 = input("Would you like to save data to your local drive or upload to RDS? pleae type 'local' or 'RDS':")
        if local_or_S3 == "local":

            bot.store_data_locally(my_dict, Postcode)
            print("data Stored locally")
            break

        elif local_or_S3 == "RDS":

            bot.upload_file_to_RDS(dataframe, file_name[-8:-5])
            print("data uploaded to RDS")
            break

        else:
            print("Im sorry, I didnt understand :S")
        
    print("finished")
    
