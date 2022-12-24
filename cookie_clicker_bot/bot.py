import re
from datetime import datetime, timedelta
from decimal import Decimal
from threading import Timer
from typing import Any, Callable

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

COOKIE_GAME_URL = 'https://orteil.dashnet.org/experiments/cookie/'


def extract_price(text: str) -> str:
    result = re.search(r'[0-9,.]+', text)
    return result and result.group() or ''


def format_price(price: str) -> str:
    return price.replace(',', '_')


def get_tag_text_content(tag: WebElement) -> str:
    if tag.is_displayed():
        return tag.text

    return tag.parent.execute_script('return arguments[0].textContent', tag)


def schedule_action(interval: float, function: Callable[..., Any]) -> Timer:
    timer = Timer(interval, function)
    timer.start()
    return timer


class CookieBot:
    def __init__(self, browser: WebDriver) -> None:
        self.browser = browser
        self.browser.get(COOKIE_GAME_URL)
        self.browser.maximize_window()

        self.cookie = browser.find_element(By.ID, 'cookie')

    def _list_available_items(self) -> dict[str, Any]:
        store_items = self.browser.find_elements(
            By.CSS_SELECTOR, 'div#store div[class=""]'
        )

        consumable_items = {}
        for item in store_items:
            id = item.get_attribute('id')

            description_tag = item.find_element(By.TAG_NAME, 'b')
            item_description = get_tag_text_content(description_tag)

            price = extract_price(item_description)
            consumable_items[id] = Decimal(format_price(price))

        return consumable_items

    def _get_more_expensive_item(self, items: dict[str, Any]) -> str:
        if not items:
            return ''

        return max(items, key=items.get).strip()  # type: ignore

    def _buy_item(self, id: str) -> None:
        if not id:
            return
        self.browser.find_element(By.ID, id).click()

    def _buy_more_expensive_item(self) -> None:
        items = self._list_available_items()
        self._buy_item(self._get_more_expensive_item(items))

    def run(self, duration: timedelta, upgrade_delay: int = 5) -> None:
        time_end = datetime.now() + duration
        timer = schedule_action(upgrade_delay, self._buy_more_expensive_item)

        while datetime.now() < time_end:
            self.cookie.click()

            if not timer.is_alive():
                timer = schedule_action(
                    upgrade_delay, self._buy_more_expensive_item
                )
