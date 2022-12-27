from datetime import timedelta
from decimal import Decimal

import pytest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from cookie_clicker_bot.bot import CookieBot


@pytest.fixture(scope='session')
def bot() -> CookieBot:
    return CookieBot(webdriver.Chrome())


def test_access_cookie_clicker_game(bot: CookieBot) -> None:
    assert 'Cookie Clicker' in bot.browser.title


def test_must_not_return_any_upgrades_available_before_the_game_starts(
    bot: CookieBot,
) -> None:
    assert '0 cookies' in bot.browser.title
    assert bot._get_upgrades_available() == {}


def test_get_upgrades_available_when_you_have_enough_coins(
    bot: CookieBot,
) -> None:
    for _ in range(15):
        bot._click_on_cookie()

    bot.browser.implicitly_wait(1)

    assert bot._get_upgrades_available()


@pytest.mark.parametrize(
    ['items', 'expected'],
    [
        ({'buyCursor': Decimal(15), 'buyGrandma': Decimal(100)}, 'buyGrandma'),
        ({}, ''),
    ],
)
def test_get_more_expensive_upgrade(
    bot: CookieBot, items: dict[str, Decimal], expected: str
) -> None:
    result = bot._get_more_expensive_upgrade(items)
    assert result == expected


def test_buy_upgrade_with_invalid_id(bot: CookieBot) -> None:
    with pytest.raises(NoSuchElementException):
        bot._buy_upgrade('#$%@')


def test_buy_more_expensive_upgrade(
    bot: CookieBot,
) -> None:
    for _ in range(100):
        bot._click_on_cookie()

    bot.browser.implicitly_wait(1)
    most_expensive = bot._get_more_expensive_upgrade(
        bot._get_upgrades_available()
    )

    bot._buy_more_expensive_upgrade()
    bot.browser.implicitly_wait(1)

    amount = int(
        bot.browser.find_element(
            By.CSS_SELECTOR, f'#{most_expensive} > .amount'
        ).text
    )

    assert amount == 1


@pytest.mark.parametrize(
    ['duration', 'upgrade_delay'],
    [
        (timedelta(minutes=0), 0),
        (timedelta(minutes=-1), 0),
        (timedelta(minutes=0), -1),
    ],
)
def test_bot_does_not_perform_clicks_when_duration_and_delay_are_invalid(
    bot: CookieBot, duration: timedelta, upgrade_delay: int
) -> None:
    title_before = bot.browser.title

    bot.run(duration, upgrade_delay)

    title_after = bot.browser.title

    assert title_before == title_after
