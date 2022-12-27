from datetime import timedelta

from selenium import webdriver

from cookie_clicker_bot.bot import CookieBot


def main() -> None:
    cookie_bot = CookieBot(webdriver.Chrome())
    cookie_bot.run(timedelta(minutes=1))


if __name__ == '__main__':
    main()
