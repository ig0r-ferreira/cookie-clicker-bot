# Cookie Clicker Bot

![Cookie Clicker Bot](assets/cookie_bot.gif)

Auto click bot for [Cookie Clicker](https://orteil.dashnet.org/experiments/cookie/) online game.

## Requirements

- 3.10 >= [Python](https://www.python.org/) version < 3.11
- [ChromeDriver](https://chromedriver.chromium.org/downloads) - Download it and set the path to it in your PATH environment variable
- [git](https://git-scm.com/)
- [pipx](https://pypa.github.io/pipx/)
  

## How to install or just run

### Run from a temporary installation

```
pipx run --spec git+https://github.com/ig0r-ferreira/cookieclicker.git cookieclicker 1
```

### Install

```
pipx install git+https://github.com/ig0r-ferreira/cookieclicker.git
```

You will now be able to run the application from anywhere on your system.

## Commands

```
cookieclicker -h                    # See the help                       
cookieclicker 1                     # Run for 1 minute
cookieclicker 1 -delay 5            # Run for 1 minute buying items every 5 seconds
```
