import re
from datetime import datetime, timedelta
from decimal import Decimal

import schedule
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

COOKIE_GAME_URL = 'https://orteil.dashnet.org/experiments/cookie/'


def extract_price(text: str) -> str:
    result = re.search(r'[0-9,.]+', text)
    return result.group() if result else ''


def format_price(price: str) -> str:
    return price.replace(',', '_')


class CookieBot:
    def __init__(self, browser: WebDriver) -> None:
        self.browser = browser
        self.browser.maximize_window()
        self.browser.get(COOKIE_GAME_URL)

        cookie_locator, store_locator = (By.ID, 'cookie'), (By.ID, 'store')
        self._wait_elements(10, cookie_locator, store_locator)

        self.cookie = browser.find_element(*cookie_locator)

    def _wait_elements(self, timeout: int, *locators: tuple[str, str]) -> None:
        wait = WebDriverWait(self.browser, timeout)
        wait.until(EC.all_of(*map(EC.presence_of_element_located, locators)))

    def _get_upgrades_available(self) -> dict[str, Decimal]:
        upgrade_shop = self.browser.find_elements(
            By.CSS_SELECTOR, 'div#store div[class=""]'
        )

        return {
            upgrade.get_attribute('id'): Decimal(
                format_price(
                    extract_price(upgrade.find_element(By.TAG_NAME, 'b').text)
                )
            )
            for upgrade in upgrade_shop
        }

    def _get_more_expensive_upgrade(self, items: dict[str, Decimal]) -> str:
        return max(items, key=items.get, default='').strip()  # type: ignore

    def _buy_upgrade(self, id: str) -> None:
        self.browser.find_element(By.ID, id).click()

    def _buy_more_expensive_upgrade(self) -> None:
        if upgrades := self._get_upgrades_available():
            self._buy_upgrade(self._get_more_expensive_upgrade(upgrades))

    def _click_on_cookie(self) -> None:
        self.cookie.click()

    def run(self, duration: timedelta, upgrade_delay: int = 5) -> None:
        if duration.total_seconds() <= 0 or upgrade_delay <= 0:
            return

        time_end = datetime.now() + duration

        schedule.every(upgrade_delay).seconds.until(duration).do(
            self._buy_more_expensive_upgrade
        )

        while datetime.now() < time_end:
            self._click_on_cookie()
            schedule.run_pending()

        schedule.clear()

    def __del__(self) -> None:
        self.browser.quit()
