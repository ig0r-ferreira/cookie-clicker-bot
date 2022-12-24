from datetime import datetime, timedelta

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

COOKIE_GAME_URL = 'https://orteil.dashnet.org/experiments/cookie/'
DURATION_IN_MINUTES = 1


def main(browser: WebDriver) -> None:
    browser.get(COOKIE_GAME_URL)
    browser.maximize_window()

    cookie = browser.find_element(By.ID, 'cookie')
    time_end = datetime.now() + timedelta(minutes=DURATION_IN_MINUTES)

    while datetime.now() < time_end:
        cookie.click()

    browser.quit()


if __name__ == '__main__':
    main(webdriver.Chrome())
