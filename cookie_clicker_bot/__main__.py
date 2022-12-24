from datetime import timedelta

from selenium import webdriver

from cookie_clicker_bot.bot import CookieBot


def main() -> None:
    CookieBot(webdriver.Chrome()).play(timedelta(minutes=1))


if __name__ == '__main__':
    main()
