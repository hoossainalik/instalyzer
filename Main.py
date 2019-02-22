"""
Module: Instagram Scrapper
Author: Hussain Ali Khan
Version: 1.0.1
Last Modified: 27/11/2018 (Tuesday)
"""

from InstagramScrapper import InstaScrapper

if __name__ == "__main__":
    scrapper = InstaScrapper()
    driver_args = []
    driver_path = "/home/hussainali/chromedriver"
    scrapper.init_scrapper(driver_path, driver_args)
    scrapper.start_scrapper()
    scrapper.close_scrapper()



