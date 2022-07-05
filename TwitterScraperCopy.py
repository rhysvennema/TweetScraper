import csv
from getpass import getpass
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from msedge.selenium_tools import Edge, EdgeOptions


def run(company, url):
    # create instance of webdriver
    options = EdgeOptions()
    options.use_chromium = True
    options.add_argument(
        "user-data-dir=C:\\Users\\rhysv\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default")
    options.add_argument("profile-directory=Default")
    options.binary_location = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    driver = Edge(options=options,
                  executable_path='C:/MSEdgeSelenium/msedgedriver.exe')

    # Open page
    driver.get('twitter.com/home')
    # Username

    # Login

    # Delay for Testing Purposes
    sleep(10)


def get_tweet_data(card):
    # Extract data from tweet card
    username = card.find_element_by_xpath('.//span').text
    handle = card.find_element_by_xpath('.//span[contains(text(), "@")]').text
    try:
        postdate = card.find_element_by_xpath(
            './/time').get_attribute('datetime')
    except NoSuchElementException:
        return
    comment = card.find_element_by_xpath('.//dive[2]/div[2]/div[1]').text
    responding = card.find_element_by_xpath('.//div[2]/div[2]/div[2]').text
    text = comment + responding
    reply_cnt = card.find_element_by_xpath('.//div[@data-testid="reply"]').text
    retweet_cnt = card.find_element_by_xpath(
        './/div[@data-testid="reply"]').text
    like_cnt = card.find_element_by_xpath('.//div[@data-testid="like"]').text

    tweet = (username, handle, postdate, text,
             reply_cnt, retweet_cnt, like_cnt)
    return tweet
