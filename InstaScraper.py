from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from msedge.selenium_tools import Edge, EdgeOptions

import Password


def run(company, url):
    # Create instance of webdriver
    options = EdgeOptions()
    options.use_chromium = True
    driver = Edge(options=options)

    # Login Sequence
    open_page(driver, url)

    # Follower Count
    followers = driver.find_element_by_xpath(
        f'//a[@href="/{url}/followers/"]/div/span').get_attribute('title')
    print(f'{followers} followers')

    # Scrolling
    scrolldown = driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);var scrolldown=document.body.scrollHeight;return scrolldown;")
    match = False
    while(match == False):
        last_count = scrolldown
        sleep(5)
        scrolldown = driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);var scrolldown=document.body.scrollHeight;return scrolldown;")
        if last_count == scrolldown:
            match = True

    # Scrapes Post URL
    post_data = []
    page_cards = driver.find_elements_by_tag_name('a')
    for card in page_cards:
        post = card.get_attribute('href')
        if '/p/' in post:
            post_data.append(post)

    # get Engagement and Date

        # Testing purposes
    print(len(post_data))
    sleep(100)
    driver.close()


def open_page(driver, url):
    # Open page
    driver.get(f'https://www.instagram.com/')
    driver.maximize_window()
    sleep(5)  # Longer because insta doesn't like bots

    # Username & Password
    username = driver.find_element_by_xpath(
        '//input[@name="username"]')
    username.send_keys('PyEngagement')
    password = driver.find_element_by_xpath(
        '//input[@name="password"]')
    password.send_keys(Password.mypassword())
    password.send_keys(Keys.RETURN)
    sleep(3)

    # Company Search
    search = driver.find_element_by_xpath(
        '//input[@placeholder="Search"]')
    search.send_keys(f'{url}')
    sleep(2)
    company = driver.find_element_by_xpath(
        f'//div[text()="{url}"]')
    sleep(1)
    company.click()
    sleep(5)


def get_post_data(card, url):
    return
