from undetected_chromedriver import Chrome
from undetected_chromedriver import ChromeOptions
from bs4 import BeautifulSoup
from formating_tools import clear_number
from urllib3.exceptions import MaxRetryError


def filter_revenue_TTM(driver, symbol: str, stock_name: str) -> dict:
    # Revenue TTM
    try:
        # Getting the full html
        html = driver.page_source

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

    except OSError:
        pass


def filter_operating_expenses(driver, symbol: str, stock_name: str) -> dict:
    # Expenses TTM;

    try:

        # Getting the full html
        html = driver.page_source

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

        # making the dictionary
        date = cells_dates[0].replace('-', '/')
        operating_expenses = clear_number(cells_operating_expenses[1])
        operating_expenses = {
            "operating_expenses": operating_expenses, "date": date}
        return operating_expenses

    except MaxRetryError:
        pass


def filter_net_income(driver, symbol: str, stock_name: str) -> dict:
    # Net Income TTM
    try:

        # Getting the full html
        html = driver.page_source

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

        # making the dictionary
        date = cells_dates[0].replace('-', '/')
        operating_expenses = clear_number(cells_operating_expenses[1])
        operating_expenses = {
            "operating_expenses": operating_expenses, "date": date}
        return operating_expenses

    except MaxRetryError:
        pass


def filter_num_shares(driver, symbol: str, stock_name: str) -> dict:
    # Num Shares
    try:

        # Getting the full html
        html = driver.page_source

        cells_num_shares = []
        cells_dates = []

        soup = BeautifulSoup(html, 'html.parser')
        num_shares = soup.find("div", id="row18jqxgrid").children
        for cell in num_shares:
            cell = cell.text
            if cell:
                cells_num_shares.append(cell)

        # DATES
        dates_row = soup.find("div", id="columntablejqxgrid").children
        for cell in dates_row:
            cell = cell.text
            if cell:
                cells_dates.append(cell)

        # deletes the first column, which doesn't have dates
        cells_dates.pop(0)

        # making the dictionary
        date = cells_dates[0].replace('-', '/')
        operating_expenses = clear_number(cells_num_shares[1])
        operating_expenses = {
            "operating_expenses": operating_expenses, "date": date}
        return operating_expenses

    except MaxRetryError:
        pass


def filter_selling_gen_admin(driver, symbol: str, stock_name: str) -> dict:
    # SG&A
    try:

        # Getting the full html
        html = driver.page_source

        # SG&A
        cells_S_G_A = []
        cells_dates = []

        soup = BeautifulSoup(html, 'html.parser')
        sga = soup.find("div", id="row4jqxgrid").children
        for cell in sga:
            cell = cell.text
            if cell:
                cells_S_G_A.append(cell)

        # DATES
        dates_row = soup.find("div", id="columntablejqxgrid").children
        for cell in dates_row:
            cell = cell.text
            if cell:
                cells_dates.append(cell)

        # deletes the first column, which doesn't have dates
        cells_dates.pop(0)
        # making the dictionary
        date = cells_dates[0].replace('-', '/')
        sga = clear_number(cells_S_G_A[1])
        # making the dictionary
        sga = {
            "sga":  sga, "date": date}

        return sga
    except MaxRetryError:
        pass


def scraper(symbol: str, stock_name: str):
    revenue = filter_revenue_TTM(
        driver=driver, symbol=symbol, stock_name=stock_name)

    # Webdriver Settings
    options = ChromeOptions()
    # Sesion without UI
    options.add_argument("--headless")
    options.add_argument("--disable-javascript")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-images")

    # Driver sesion initialization
    driver = Chrome(options=options)
    URL = str(
        f"https://www.macrotrends.net/stocks/charts/%7B{symbol}/{stock_name}/income-statement?freq=Q")
    driver.get(URL)
    driver.implicitly_wait(0)

    revenue = filter_revenue_TTM(
        driver=driver, symbol=symbol, stock_name=stock_name)
    operatin_exp = filter_operating_expenses(
        driver=driver, symbol=symbol, stock_name=stock_name)
    net_income = filter_net_income(
        driver=driver, symbol=symbol, stock_name=stock_name)
    num_shares = filter_num_shares(
        driver=driver, symbol=symbol, stock_name=stock_name)
    sga = filter_selling_gen_admin(
        driver=driver, symbol=symbol, stock_name=stock_name)
    driver.__del__()
    driver.quit()
    finance_variables = {"revenue": revenue,
                         "operatin_exp": operatin_exp,
                         "net_income": net_income,
                         "num_shares": num_shares,
                         "sga": sga
                         }
    return finance_variables


if __name__ == '__main__':
    pass
