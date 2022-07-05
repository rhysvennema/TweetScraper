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
        f'//a[@href="/{url}/followers"]/span/span').text
    #print(f'{followers} followers')

    # Tweet Scraper
    tweet_data = []
    tweet_ids = set()
    scrolling = True

    while scrolling:
        page_cards = driver.find_elements_by_xpath(
            '//article[@data-testid="tweet"]')
        for card in page_cards[-15:]:
            tweet = get_tweet_data(card, url)
            if tweet:
                tweet_id = ''.join(tweet)
                if tweet_id not in tweet_ids:
                    tweet_ids.add(tweet_id)
                    tweet_data.append(tweet)

        scroll_attempt = 0
        last_position = driver.execute_script("return window.pageYOffset;")
        while True:
            # Check scroll position
            driver.execute_script(
                'window.scrollTo(0, document.body.scrollHeight);')
            sleep(2)
            curr_position = driver.execute_script("return window.pageYOffset;")
            if last_position == curr_position:
                scroll_attempt += 1

                # end of scroll region
                if scroll_attempt >= 3:
                    scrolling = False
                    break
                else:
                    sleep(2)  # attempt to scroll again
            else:
                last_position = curr_position
                break

    # close the web driver
    driver.close()

    # csv data
    return (company, followers, extract(0, tweet_data), extract(1, tweet_data))


def open_page(driver, url):
    # Open page
    driver.get(f'https://www.twitter.com/login')
    driver.maximize_window()
    sleep(1)
    # Username
    username = driver.find_element_by_xpath(
        '//input[@autocomplete="username"]')
    username.send_keys('PyEngagement')
    next = driver.find_element_by_xpath(
        '//span[text()="Next"]')
    next.click()
    sleep(1)
    # Login
    password = driver.find_element_by_xpath(
        '//input[@name="password"]')
    password.send_keys(Password.mypassword())
    password.send_keys(Keys.RETURN)
    sleep(1)
    # Company Search
    search = driver.find_element_by_xpath(
        '//input[@placeholder="Search Twitter"]')
    search.send_keys(f'{url}')
    search.send_keys(Keys.RETURN)
    sleep(1)
    people = driver.find_element_by_xpath('//span[text()="People"]')
    people.click()
    sleep(1)
    company = driver.find_element_by_xpath(f'//a[@href="/{url}"]')
    company.click()
    sleep(1)


def get_tweet_data(card, url):
    replys = card.find_element_by_xpath(
        './/div[@data-testid="reply"]').text
    retweets = card.find_element_by_xpath(
        './/div[@data-testid="retweet"]').text
    likes = card.find_element_by_xpath(
        './/div[@data-testid="like"]').text
    try:  # Gets rid of ads
        date = card.find_element_by_xpath(
            './/time').get_attribute('datetime')
        date = date[:10]
    except NoSuchElementException:
        return

    isTweet = True
    try:
        retweet = card.find_element_by_xpath(
            './/span[@data-testid="socialContext"]'
        )
        return
    except NoSuchElementException:
        isTweet = True

    # try:  # Gets rid of retweets
        # retweet = card.find_element_by_xpath(
        # './/span[contains(text()," Retweeted")])'
        # )
        # return
    # except NoSuchElementException:
        # print('tweet')

    engagement = [replys, retweets, likes]
    engagement = {x.replace(',', '') for x in engagement}  # removes commas
    count = 0
    for eng in engagement:
        if eng == "":
            count += 0
        elif 'K' in eng:
            step = eng.replace('K', '')
            count += int(float(step) * 1000)
        else:
            count += int(eng)

    tweet_data = (str(count), date)
    return tweet_data


def extract(elementn, list):
    return [item[elementn] for item in list]
