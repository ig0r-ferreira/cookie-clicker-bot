from datetime import timedelta

from selenium import webdriver
from selenium.common.exceptions import NoSuchWindowException

from cookie_clicker_bot.bot import CookieBot


def main() -> None:
    try:
        CookieBot(webdriver.Chrome()).run(timedelta(minutes=1))
    except NoSuchWindowException:
        print('Bot execution stopped, program will exit.')


if __name__ == '__main__':
    main()
