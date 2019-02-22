"""
Module: Instagram Scrapper
Author: Hussain Ali Khan
Version: 1.0.2
Last Modified: 28/11/2018 (Wednesday)
"""

from bs4 import BeautifulSoup
from SeleniumHelper import SeleniumBrowserHelper
from PostScrapper import PostScrapper
from PostScrapper import PostDetails
import pandas as pd
import json
import time
import FileHandler as fh


class InstaDetails:
    def __init__(self):
        self.username = None
        self.verified = None
        self.name = None
        self.bio = None
        self.website = None
        self.no_of_posts = None
        self.no_of_followers = None
        self.no_of_following = None
        self.posts = None
        self.data = None


class InstaScrapper(InstaDetails):
    posts_count = 0

    def __init__(self):
        self.html = None
        self.helper = None
        self.chrome_driver_path = None
        self.chrome_options = None
        self.soup = None
        self.instagram_url = "https://www.instagram.com"
        self.url_to_visit = ""
        self.search_value = ""
        self.selected = None
        self.internet_connected = False
        self.instagram_reachable = False
        self.scrappable = False
        self.details_extracted = False
        self.characteristics = {"profile": False, "location": False, "hashtag": False}
        self.posts_data = PostDetails()

    def insta_search(self):
        self.helper.open_url(self.instagram_url + "/instagram/")
        self.helper.wait_until(delay=5, type="-class", arg="_9eogI")
        self.load_page_content()
        insta_search = self.helper.get_element("-class", "XTCLo")
        self.search_value = input("Enter Something To Search On Instagram: ")
        insta_search.send_keys(self.search_value)
        self.helper.wait_until(delay=5, type="-class", arg="fuqBx")
        self.load_page_content()
        search_response = self.soup.find_all('a', {'class': 'yCE8d'})

        choices = {}

        for i, s in enumerate(search_response):
            current_link = s['href']
            current_value = s.find('span', {'class': 'Ap253'}).get_text()
            current_response = [current_value, current_link]
            choices[i] = current_response

        print("Following Are The Top Results Against Your Search: ")
        print("<---------Search Results-------->")
        for key, value in choices.items():
            print("\t", key+1, ".", value[0])
        print("<------------------------------->")
        option = int(input("Please Choose An Option From Search Results\nChoice: "))

        self.selected = choices[option-1]

        self.url_to_visit = self.selected[1]

        self.check_n_set_url_characteristics(self.url_to_visit)

    def start_fetching(self):
        if self.characteristics["profile"]:
            print("Fetching Data From Instagram For Profile: " + self.selected[0] + " !!!")
            self.helper.open_url(self.instagram_url + self.url_to_visit)
            self.helper.wait_until(delay=10, type="-class", arg="_9eogI")
            self.load_page_content()
            self.extract_details(1)
            self.print_details(1)
            self.fetch_posts()
            self.save_details(1)
            self.save_as_csv(1)
            self.save_as_json(1)

        elif self.characteristics["location"]:
            print("Fetching Data From Instagram For Location: " + self.selected[0] + " !!!")
            self.helper.open_url(self.instagram_url + self.url_to_visit)
            self.helper.wait_until(delay=10, type="-class", arg="_9eogI")
            self.load_page_content()
            self.extract_details(3)
            self.print_details(3)
            self.fetch_posts()
            self.save_details(3)
            self.save_as_csv(3)
            self.save_as_json(3)

        elif self.characteristics["hashtag"]:
            print("Fetching Data From Instagram For Hashtag: " + self.selected[0] + " !!!")
            self.helper.open_url(self.instagram_url + self.url_to_visit)
            self.helper.wait_until(delay=10, type="-class", arg="_9eogI")
            self.load_page_content()
            self.extract_details(2)
            self.print_details(2)
            self.fetch_posts()
            self.save_details(2)
            self.save_as_csv(2)
            self.save_as_json(2)

    def extract_details(self, choice):
        if choice == 1:
            if self.scrappable:

                username = self.soup.find('h1', {'class': 'AC5d8'})
                if username is None:
                    self.username = "Not Available"
                else:
                    self.username = username.get_text()

                name = self.soup.find('h1', {'class': 'rhpdm'})
                if name is None:
                    self.name = "Not Available"
                else:
                    self.name = name.get_text()

                bio = self.soup.find('div', {'class': '-vDIg'}).span
                if bio is None:
                    self.bio = "Not Available"
                else:
                    self.bio = bio.get_text()

                verified = self.soup.find('span', {'class': 'mrEK_'})
                if verified is not None and verified.get_text() == "Verified":
                    self.verified = True
                else:
                    self.verified = False

                profile_statistics = self.soup.find_all('span', {'class': 'g47SY'})
                self.no_of_posts = profile_statistics[0].get_text()
                self.no_of_followers = profile_statistics[1].get_text()
                self.no_of_following = profile_statistics[2].get_text()

                website = self.soup.find('a', {'class': 'yLUwa'})
                if website is None:
                    self.website = "Not Available"
                else:
                    self.website = website.get_text()

                self.details_extracted = True

        elif choice == 2:
            name = self.soup.find('a', {'class': 'F2iT8'})
            if name is None:
                self.name = "Not Available"
            else:
                self.name = name.get_text()

            total_posts = self.soup.find('span', {'class': 'g47SY'})

            if total_posts is None:
                self.no_of_posts = "0"
            else:
                self.no_of_posts = total_posts.get_text()

            self.details_extracted = True

        elif choice == 3:
            name = self.soup.find('h1', {'class': 'cgig_'})
            if name is None:
                self.name = "Not Available"
            else:
                self.name = name.get_text()

            self.no_of_posts = "100"

            self.details_extracted = True
        else:
            print("Content Cannot Be Fetched At The Moment!")

    def check_n_set_url_characteristics(self, url):
        if "explore" in url:
            if "tags" in url:
                self.characteristics["hashtag"] = True
            elif "locations" in url:
                self.characteristics["location"] = True
        else:
            self.characteristics["profile"] = True

    def init_scrapper(self, c_path, c_args):
        # print("Initializing Scrapper!!!!!!")
        self.chrome_driver_path = c_path
        self.chrome_options = c_args
        self.helper = SeleniumBrowserHelper(self.chrome_driver_path, self.chrome_options)
        # print("Checking Internet Connectivity!!!!")
        self.internet_connected = self.helper.is_connected()
        # self.instagram_reachable = self.helper.is_reachable(self.instagram_url, 10)

    def start_scrapper(self):
        print("Starting Scrapper!!!!")
        if self.internet_connected:
            # if self.instagram_reachable:
                self.insta_search()
                self.scrappable = True
                self.init_posts_data()
                self.start_fetching()
                print("Fetching Completed!!!!")
                self.save_posts_data()
                time.sleep(3)
            # else:
            #     print("Instagram Access Restricted By ISP/Network Administrator")
        else:
            print("No Internet!! Please Check Your Network Connectivity!!")

    def close_scrapper(self):
        print("Closing Scrapper In 3 Seconds! Have A Nice Day!!!")
        self.helper.close_browser()
        time.sleep(3)

    def load_page_content(self):
        self.html = self.helper.get_page_source()
        self.soup = BeautifulSoup(self.html, 'html.parser')

    def save_details(self, code):

        if code == 1:
            self.data = {
                "username": self.username,
                "is_verified": self.verified,
                "name": self.name,
                "bio": self.bio,
                "website": self.website,
                "posts_count": self.no_of_posts,
                "followers_count": self.no_of_followers,
                "following_count": self.no_of_following,
                "posts": [self.posts]
            }

        elif code == 2:
            self.data = {
                "hashtag": self.name,
                "posts_count": self.no_of_posts,
                "posts": [self.posts]
            }

        elif code == 3:
            self.data = {
                "location": self.name,
                "top_100_posts": [self.posts]
            }

    def fetch_posts(self):

        total_posts = int(self.no_of_posts.replace(',', ''))

        choice = int(input("Please Select An Option For Fetching " + self.name+"'s Posts: \n\t1. Fetch All " +
                           str(total_posts) + " Posts\n\t2. Fetch Top Posts Upto A Certain Limit\nChoice: "))

        if choice == 1:
            self.get_posts(total_posts)
        elif choice == 2:
            limit = int(input("How Many Posts Due To Want To Fetch Out Of "+str(total_posts)+": "))
            self.get_posts(limit)
        else:
            print("Invalid Choice!! Please Select Again")
            time.sleep(1)
            self.fetch_posts()

    def get_posts(self, no_of_posts):
        self.posts = {}
        print("Posts: ")
        print("<--------------------------------------------------->")
        while InstaScrapper.posts_count < no_of_posts:
            self.helper.scroll_down()
            self.load_page_content()
            self.extract_posts(no_of_posts)
            time.sleep(1)
        print("<--------------------------------------------------->")
        print(str(no_of_posts)+" Posts Fetched!!!")
        self.posts = list(self.posts.values())

    def extract_posts(self, nop):
        posts = self.soup.find_all('div', {'class': 'v1Nh3'})

        for p in posts:
            p_link = p.a['href']
            post_id = p_link[3:-1]
            post = self.instagram_url + p_link
            if InstaScrapper.posts_count < nop:
                self.add_post(post_id, post)
            else:
                break

    def is_post_present(self, post_id):
        if post_id in self.posts:
            return True
        else:
            return False

    def add_post(self, post_id, post):
        if not self.is_post_present(post_id):
            self.posts[post_id] = post
            InstaScrapper.posts_count += 1
            print("Sr: "+str(InstaScrapper.posts_count)+", Id: "+post_id+", Url: "+post)
            posts_scrapper = PostScrapper(post)
            driver_args = ["--headless"]
            driver_path = "/home/hussainali/chromedriver"
            posts_scrapper.init_scrapper(driver_path, driver_args)
            post_data = posts_scrapper.start_scrapper()
            posts_scrapper.close_scrapper()
            self.add_posts_data(post_data)

    def init_posts_data(self):
        self.posts_data.source_url = []
        self.posts_data.description = []
        self.posts_data.hashtags = []
        self.posts_data.mentions = []
        self.posts_data.emojis = []
        self.posts_data.comments = []

    def add_posts_data(self, post_data):
        self.posts_data.source_url.append(post_data[0])
        self.posts_data.description.append(post_data[1])
        self.posts_data.hashtags.append(post_data[2])
        self.posts_data.mentions.append(post_data[3])
        self.posts_data.emojis.append(post_data[4])
        self.posts_data.comments.append(post_data[5])

    def save_posts_data(self):
        posts_data = {
            "post_url": self.posts_data.source_url,
            "description": self.posts_data.description,
            "hashtags": self.posts_data.hashtags,
            "mentions": self.posts_data.mentions,
            "emojis": self.posts_data.emojis,
            "comments": self.posts_data.comments
        }

        fh.save_as_csv("Posts/" + self.name + "_posts_data", posts_data)

    def print_details(self, code):
        if self.details_extracted:
            if code == 1:
                print("<------------------Profile Details------------------>")
                print("Username: @" + self.username)
                print("Verified: ", self.verified)
                print("Name: " + self.name)
                print("Bio: " + self.bio)
                print("Website: " + self.website)
                print("Total Posts: " + self.no_of_posts)
                print("Followers: " + self.no_of_followers)
                print("Following: " + self.no_of_following)
                print("<--------------------------------------------------->")
            elif code == 2:
                print("<------------------Hashtag Details------------------>")
                print("Hashtag: " + self.name)
                print("Total Posts: " + self.no_of_posts)
                print("<--------------------------------------------------->")
            elif code == 3:
                print("<------------------Location Details------------------>")
                print("Location: " + self.name)
                print("<--------------------------------------------------->")

        else:
            print("Details Not Extracted Yet!!")

    def save_as_csv(self, code):
        if code == 1:
            df = pd.DataFrame(self.data)
            df.to_csv("Profiles/" + self.name + "_data.csv")
        elif code == 2:
            df = pd.DataFrame(self.data)
            df.to_csv("Hashtags/" + self.name + "_data.csv")
        elif code == 3:
            df = pd.DataFrame(self.data)
            df.to_csv("Locations/" + self.name + "_data.csv")

    def save_as_json(self, code):
        if code == 1:
            with open("Profiles/" + self.name + "_data.json", 'w') as profile:
                json.dump(self.data, profile)
        elif code == 2:
            with open("Hashtags/" + self.name + "_data.json", 'w') as hashtag:
                json.dump(self.data, hashtag)
        elif code == 3:
            with open("Locations/" + self.name + "_data.json", 'w') as location:
                json.dump(self.data, location)

