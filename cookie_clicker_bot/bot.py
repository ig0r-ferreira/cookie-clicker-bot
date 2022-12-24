from datetime import datetime, timedelta

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

COOKIE_GAME_URL = 'https://orteil.dashnet.org/experiments/cookie/'


class CookieBot:
    def __init__(self, browser: WebDriver) -> None:
        self.browser = browser
        self.browser.get(COOKIE_GAME_URL)
        self.browser.maximize_window()

        self.cookie = browser.find_element(By.ID, 'cookie')

    def play(self, duration: timedelta) -> None:
        time_end = datetime.now() + duration

        while datetime.now() < time_end:
            self.cookie.click()
