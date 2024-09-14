from undetected_chromedriver import Chrome
from undetected_chromedriver import ChromeOptions
from bs4 import BeautifulSoup
from formating_tools import clear_number
from urllib3.exceptions import MaxRetryError
from time import sleep


def filter_revenue_TTM(html) -> dict:
    # Revenue TTM
    try:
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


def filter_operating_expenses(html) -> dict:
    # Expenses TTM;

    try:
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


def filter_net_income(html) -> dict:
    # Net Income TTM
    try:

        soup = BeautifulSoup(html, 'html.parser')

        cells_netIncome = []
        cells_dates = []

        Net_income = soup.find("div", id="row15jqxgrid").children
        for cell in Net_income:
            cell = cell.text
            if cell:
                cells_netIncome.append(cell)

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
        net_income = clear_number(cells_netIncome[1])
        net_income = {
            "net_income": net_income, "date": date}
        return net_income

    except MaxRetryError:
        pass


def filter_num_shares(html) -> dict:
    # Num Shares
    try:

        cells_num_shares = []
        cells_dates = []

        soup = BeautifulSoup(html, 'html.parser')
        num_shares = soup.find("div", id="row19jqxgrid").children
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
        num_shares = clear_number(cells_num_shares[1])
        num_shares = {
            "num_shares": num_shares, "date": date}
        return num_shares

    except MaxRetryError:
        pass


def filter_selling_gen_admin(html) -> dict:
    # SG&A
    try:

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
    try:
        # Webdriver Settings
        options = ChromeOptions()
        # Sesion without UI
        # options.add_argument("--headless")
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
            f"https://www.macrotrends.net/stocks/charts/{symbol}/{stock_name}/income-statement?freq=Q")
        driver.get(URL)
        driver.implicitly_wait(0)

        html = driver.page_source

        revenue = filter_revenue_TTM(html)
        operating_expenses = filter_operating_expenses(html)
        net_income = filter_net_income(html)
        num_shares = filter_num_shares(html)
        sga = filter_selling_gen_admin(html)

        # driver.__del__()
        # driver.quit()

        finance_variables = {"revenue": revenue,
                             "operating_expenses": operating_expenses,
                             "net_income": net_income,
                             "num_shares": num_shares,
                             "sga": sga
                             }
        print(finance_variables)
        return finance_variables

    finally:
        driver.quit()

# if __name__ == '__main__':
    # scraper('', '')
#    pass
