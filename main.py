from Property_Web_Scraper import PropertyScraper

if __name__ == "__main__":
    print("lets go")
    bot = PropertyScraper()
    print('starting..')
    bot.login()
    print('log in')
    list_links = bot.get_links()
    print("links attained")
    my_dict = bot.get_info(list_links)
    print("info Attained")
    bot.download_images(my_dict)
    print("images downloaded")
    bot.store_data(my_dict)
    print("data Stored")
    print("finished")