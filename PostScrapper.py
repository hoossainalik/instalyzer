"""
Module: Post Scrapper
Author: Hussain Ali Khan
Version: 1.0.2
Last Modified: 28/11/2018 (Wednesday)
"""

from bs4 import BeautifulSoup
from SeleniumHelper import SeleniumBrowserHelper
import time


class PostDetails:
    def __init__(self):
        self.description = None
        self.category = None
        self.source_url = None
        self.comments = None
        self.likers = None
        self.datetime_posted = None
        self.total_likes = None
        self.total_views = None
        self.hashtags = None
        self.mentions = None
        self.emojis = None


class PostScrapper(PostDetails):
    def __init__(self, post_url):
        self.html = None
        self.helper = None
        self.chrome_driver_path = None
        self.chrome_options = None
        self.soup = None
        self.instagram_url = "https://www.instagram.com"
        self.url_to_visit = post_url
        self.internet_connected = False
        self.instagram_reachable = False
        self.scrappable = False
        self.details_extracted = False

    def init_scrapper(self, c_path, c_args):
        # print("Initializing Scrapper!!!!!!")
        self.chrome_driver_path = c_path
        self.chrome_options = c_args
        self.helper = SeleniumBrowserHelper(self.chrome_driver_path, self.chrome_options)
        # print("Checking Internet Connectivity!!!!")
        self.internet_connected = self.helper.is_connected()
        # self.instagram_reachable = self.helper.is_reachable(self.instagram_url, 10)

    def start_scrapper(self):
        # print("Starting Scrapper!!!!")
        if self.internet_connected:
            # if self.instagram_reachable:
            self.scrappable = True
            self.start_fetching()
            print("Post Data Fetching Completed!!!!")
            time.sleep(1)
            return self.get_details()
        # else:
        #     print("Instagram Access Restricted By ISP/Network Administrator")
        else:
            print("No Internet!! Please Check Your Network Connectivity!!")
            return {}

    def close_scrapper(self):
        # print("Closing Scrapper In 3 Seconds! Have A Nice Day!!!")
        self.helper.close_browser()

    def start_fetching(self):
        print("Fetching Data From Instagram Post Against Url: " + self.url_to_visit + " !!!")
        self.helper.open_url(self.url_to_visit)
        self.helper.wait_until(delay=10, type="-class", arg="ltEKP")
        self.load_page_content()
        self.extract_details()
        # fh.save_as_csv()
        # fh.save_as_json()

    def load_page_content(self):
        self.html = self.helper.get_page_source()
        self.soup = BeautifulSoup(self.html, 'html.parser')

    def extract_details(self,):
        if self.scrappable:
            desc = self.soup.find('h2', {'class': '_6lAjh'})

            if desc is not None:
                description = desc.find_next_sibling("span")
            else:
                description = None

            if description is None:
                self.description = "Not Available"
            else:
                self.description = description.get_text()
                self.hashtags = [h for h in self.description.split() if h.startswith("#")]
                if self.hashtags is None:
                    self.hashtags = []
                self.mentions = [m for m in self.description.split() if m.startswith("@")]
                if self.mentions is None:
                    self.mentions = []
                self.emojis = [e for e in self.description.split() if str(e.encode('unicode-escape'))[2] == '\\']
                if self.emojis is None:
                    self.emojis = []

            post_datetime = self.soup.find('time', {'class':'_1o9PC'})

            if post_datetime is None:
                self.datetime_posted = "Not Available"
            else:
                self.datetime_posted = post_datetime["datetime"]

            # print("Description: ", self.description)
            # print("Hashtags: ", self.hashtags)
            # print("Mentions: ", self.mentions)
            # print("Emojis: ", self.emojis)
            # print("DateTime Posted: ", self.datetime_posted)

            comments = self.soup.find_all("div", {"class": "C4VMK"})

            if comments is None:
                self.comments = "Not Available"
            else:
                self.comments = []

                for c in range(1, len(comments)):

                    commentor = comments[c].h3.a
                    if commentor is not None:
                        commentor = "@"+commentor.get_text()

                    comment = comments[c].span

                    if comment is not None:
                        comment = comment.get_text()

                    if commentor is not None and comment is not None:
                        self.comments.append([commentor, comment])

            # print("Comments: ", self.comments)

            self.details_extracted = True

        else:
            print("Post Content Cannot Be Fetched At The Moment!")

    def get_details(self):
        post_details = [
            [self.url_to_visit],
            [self.description],
            self.hashtags,
            self.mentions,
            self.emojis,
            self.comments
        ]

        return post_details
