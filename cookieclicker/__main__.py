from argparse import ArgumentParser, ArgumentTypeError
from datetime import timedelta

from selenium import webdriver

from cookieclicker.bot import CookieBot


def value_greater_than_zero(string) -> float:
    try:
        value = float(string)
    except ValueError:
        raise ArgumentTypeError(f'{string!a} is not a number.')
    else:
        if value <= 0:
            raise ArgumentTypeError(f'{string!a} is not greater than zero.')
        return value


def main() -> None:
    parser = ArgumentParser(
        description='Auto click bot for Cookie Clicker online game.'
    )
    parser.add_argument(
        'duration', help='Duration in minutes.', type=value_greater_than_zero
    )
    parser.add_argument(
        '-delay',
        help='Delay until the next purchase of items. Default is %(default)d.',
        type=value_greater_than_zero,
        default=3,
    )
    args = vars(parser.parse_args())

    cookie_bot = CookieBot(webdriver.Chrome())
    cookie_bot.run(
        duration=timedelta(minutes=args['duration']),
        upgrade_delay=args['delay'],
    )
    print(cookie_bot.get_performance_info())


if __name__ == '__main__':
    main()
