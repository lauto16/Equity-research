from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc


def TTM_revenue(driver):
    "Revenue TTM"
    URL = 'https://www.macrotrends.net/stocks/charts/WDAY/workday/operating-margin'

    try:
        # Open URL

        driver.get(URL)

        # Getting the full html
        html = driver.page_source

    finally:
        try:
            driver.quit()
        except OSError as e:
            print('el error fue: ', e)
    # DEBUG
    with open('./Debug/debug.txt', 'w')as debug:
        debug.write(html)


def income_statement(driver):
    # Expenses TTM; Net Income TTM; Num Shares; SG&A

    URL = "https://www.macrotrends.net/stocks/charts/AAPL/apple/income-statement?freq=Q"
    try:
        # Open URL
        driver.get(URL)

        # Getting the full html
        html = driver.page_source

    finally:
        try:
            driver.quit()
        except OSError as e:
            print('el error fue: ', e)
    # DEBUG
    with open('./Debug/debug1.txt', 'w')as debug:
        debug.write(html)


def total_assets(driver):
    # Expenses TTM; Net Income TTM; Num Shares; SG&A

    URL = "https://www.macrotrends.net/stocks/charts/AAPL/apple/total-assets"
    try:
        # Open URL
        driver.get(URL)

        # Getting the full html
        html = driver.page_source

    finally:
        try:
            driver.quit()
        except OSError as e:
            print('el error fue: ', e)
    # DEBUG
    with open('./Debug/debug2.txt', 'w')as debug:
        debug.write(html)


def main():
    # EXCEL Variables:
    tag = ''
    complete_tag = ''

    # Webdriver Settings
    options = uc.ChromeOptions()
    options.headless = True  # Sesion without UI
    options.add_argument("--headless")

    # Driver sesion initialization
    driver = uc.Chrome()
    # setting the sleep times to 0 when not necessary
    driver.implicitly_wait(0)

    total_assets(driver)


if __name__ == '__main__':
    main()
