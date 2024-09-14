from undetected_chromedriver import Chrome
from undetected_chromedriver import ChromeOptions
from bs4 import BeautifulSoup
from formating_tools import clear_number
from urllib3.exceptions import MaxRetryError


def filter_revenue_TTM(driver, symbol: str, stock_name: str) -> dict:
    "Revenue TTM"
    URL = str(f"https://www.macrotrends.net/stocks/charts/{
              symbol}/{stock_name}/income-statement?freq=Q")
    try:
        # Open URL

        driver.get(URL)

        # Getting the full html
        html = driver.page_source
        driver.quit()
        soup = BeautifulSoup(html, 'html.parser')

        cells_revenue = []
        cells_dates = []

        soup = BeautifulSoup(html, 'html.parser')
        revenue_row = soup.find("div", id="row0jqxgrid")

        for cell in revenue_row:
            cell = cell.text
            if cell:
                cells_revenue.append(cell)

        # DATES
        dates_row = soup.find("div", id="columntablejqxgrid").children
        for cell in dates_row:
            cell = cell.text
            if cell:
                cells_dates.append(cell)
        # deletes the first column, which doesn't have dates
        cells_dates.pop(0)

        # making the dictionary
        revenue = clear_number(cells_revenue[1])
        date = cells_dates[0].replace('-', '/')
        revenue = {"revenue": revenue, "date": date}
        return revenue

    except MaxRetryError:
        pass
    finally:
        driver.quit()


def filter_operating_expenses(driver) -> dict:
    # Expenses TTM;

    URL = "https://www.macrotrends.net/stocks/charts/AAPL/apple/income-statement?freq=Q"
    try:
        # Open URL
        driver.get(URL)
        # Getting the full html
        html = driver.page_source
        driver.quit()

        soup = BeautifulSoup(html, 'html.parser')
        cells_operating_expenses = []
        cells_dates = []

        operating_row = soup.find("div", id="row6jqxgrid").children
        for cell in operating_row:
            cell = cell.text
            if cell:
                cells_operating_expenses.append(cell)

        # DATES
        dates_row = soup.find("div", id="columntablejqxgrid").children
        for cell in dates_row:
            cell = cell.text
            if cell:
                cells_dates.append(cell)
        # deletes the first column, which doesn't have dates
        cells_dates.pop(0)
        operating_expenses = clear_number(cells_operating_expenses[1])
        # making the dictionary
        operating_expenses = {
            "operating_expenses":  operating_expenses, "date": cells_dates[0]}
        return operating_expenses

    except MaxRetryError:
        pass
    finally:
        driver.quit()


def total_assets(driver):
    # Expenses TTM; Net Income TTM; Num Shares; SG&A

    URL = "https://www.macrotrends.net/stocks/charts/AAPL/apple/total-assets"
    try:
        # Open URL
        driver.get(URL)

        # Getting the full html
        html = driver.page_source
    except OSError:
        pass
    finally:
        driver.quit()
    # DEBUG
    with open('./Debug/debug2.txt', 'w')as debug:
        debug.write(html)


def main(symbol: str, stock_name: str) -> dict:

    # Webdriver Settings
    options = ChromeOptions()
    # Sesion without UI
    # options.add_argument("--headless")
    options.add_argument("--disable-javascript")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("start-maximized")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-images")

    # Driver sesion initialization
    driver = Chrome(options=options)

    revenue = filter_revenue_TTM(
        driver=driver, symbol=symbol, stock_name=stock_name)
    # operatin_exp = filter_operating_expenses(driver)

    # temporary
    return revenue


if __name__ == '__main__':
    pass
