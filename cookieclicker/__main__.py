from datetime import timedelta

from selenium import webdriver

from cookieclicker.bot import CookieBot


def main() -> None:
    cookie_bot = CookieBot(webdriver.Chrome())
    cookie_bot.run(timedelta(minutes=1))
    print(cookie_bot.get_performance_info())


if __name__ == '__main__':
    main()
