"""
Module: Selenium Helper
Author: Hussain Ali Khan
Version: 1.0.1
Last Modified: 27/11/2018 (Tuesday)
"""

from selenium import webdriver  # For opening webdriver for specific browser
from selenium.webdriver.common.by import By    # For selecting html code
from selenium.webdriver.support.ui import WebDriverWait  # For Adding Implicit Or Explicit Wait Functionality
from selenium.webdriver.support import expected_conditions as ec  # For Detecting An Expected Condition
from selenium.common.exceptions import TimeoutException  # For Timing Out If Fetching Takes Too Much Time
from selenium.webdriver.common.keys import Keys # For necessary browser action such as scrolling
from urllib.request import urlopen  # For Checking Internet Connectivity


class SeleniumBrowserHelper:
    """ Helper Class For Complementing Browser Functionality In Selenium """

    def __init__(self,b_path, b_args):
        """  Default Constructor Of Selenium Helper Class"
        :param b_path: Path Of The Driver For Browser
        :param b_args: A List Of Arguments For Browser
        """
        if len(b_args) > 0:
            chrm_optns = webdriver.ChromeOptions()
            for arg in b_args:
                chrm_optns.add_argument(arg)

            self.browser = webdriver.Chrome(b_path, chrome_options=chrm_optns)

        else:
            self.browser = webdriver.Chrome(b_path)

    def open_url(self,url):
        """ Method To Open The Provided URL In Browser
        :param url: Url Of The Webpage to be Opened
        :return: None
        """
        self.browser.get(url)

    def scroll_down(self):
        """ Method For Implementing Scroll Down Functionality In Browser
        :return: None
        """
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # root_element = self.browser.find_element_by_tag_name("html")
        # root_element.send_keys(Keys.DOWN)

    def get_page_source(self):
        """ Method To Get Page Source Html
        :return: Html Of The Current Webpage Opened In The Browser
        """
        return self.browser.page_source

    def is_connected(self, url="http://www.google.com", time_out=1):
        """ Method To Check Internet Connectivity By Visiting Google
        :param url: Optional Argument To Check Internet Connectivity By Visiting A Url
        :param time_out: Timeout In Seconds
        :return: Boolean Value Stating Whether Internet is Connected Or Not
        """
        try:
            urlopen(url, timeout=time_out)
            # print("Connectivity Checked!!")
            return True
        except OSError:
            return False

    def is_reachable(self, url):
        """ Method To Check Whether A Url Is Reachable
        :param url: Url of the webpage whose reachability is to be checked
        :return: status of reachability (Boolean)
        """
        return self.is_connected(url)

    def wait_until(self, delay, type, arg):
        """ Method For Waiting Implicitly Until A Particular Element Is Loaded In A Webpage
        :param type: Type Of Selection Criteria For Element
        :param arg: Name Of The Selection Variable
        :return: None
        """
        type_dictionary = {
            "-id": By.ID,
            "-tag": By.TAG_NAME,
            "-class": By.CLASS_NAME,
            "-xpath": By.XPATH,
            "-name": By.NAME,
            "-css": By.CSS_SELECTOR,
            "-link": By.LINK_TEXT
        }

        try:
            WebDriverWait(self.browser, delay).until(ec.presence_of_element_located((type_dictionary[type], arg)))
            # print("Page is ready!")
        except TimeoutException:
            print("Fetching Profile Took Much Time!")

    def wait(self, delay):
        """ Method Of Implementing Explicit Delay
        :param delay: Time In Seconds To Wait
        :return: None
        """

    def get_element(self, type, arg):
        """ Method To Get An Html Element Against Given Criteria
        :param type: Type Of Selection Criteria For Element
        :param arg: Name Of The Selection Variable
        :return: Html Element Against The Given Criteria (Html Object)
        """
        type_dictionary = {
            "-id": By.ID,
            "-tag": By.TAG_NAME,
            "-class": By.CLASS_NAME,
            "-xpath": By.XPATH,
            "-name": By.NAME,
            "-css": By.CSS_SELECTOR,
            "-link": By.LINK_TEXT
        }

        matched_element = self.browser.find_element(type_dictionary[type], arg)
        return matched_element

    def close_browser(self):
        """  Method For Closing Browser Instance
        :return: None
        """
        self.browser.quit()
