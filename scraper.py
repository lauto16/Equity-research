from undetected_chromedriver import Chrome
from undetected_chromedriver import ChromeOptions
from bs4 import BeautifulSoup
from formating_tools import clear_number
from formating_tools import special_clear
from selenium.common.exceptions import TimeoutException


def filter_operating_expenses(html) -> dict:
    # Expenses;

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
    operating_expensesTTM = 0
    for i in range(1, 5):
        operating_expensesTTM += clear_number(cells_operating_expenses[i])

    operating_expensesTTM = {
        "operating_expensesTTM": operating_expensesTTM, "date": date}
    return operating_expensesTTM


def filter_num_shares(html) -> dict:
    # Num Shares

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


def filter_selling_gen_admin(html) -> dict:

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
    # when loading the page, sga appears to be a float at macrotrends, but once it's fully loaded
    # it refreshes into an int value changing from, for example: 6.320 to 6320, by removing the call
    # to the clear function we prevent this conversion
    sga = special_clear(cells_S_G_A[1])
    # making the dictionary
    sga = {
        "sga":  sga, "date": date}

    return sga


def filter_total_assets(html) -> dict:
    # Total Assets
    soup = BeautifulSoup(html, 'html.parser')
    tables = soup.find_all("table", class_="historical_data_table table")
    # stands for the first table which contains date and total assets
    total_assets_quarterly = tables[1]

    fst_row = total_assets_quarterly.find_all("td")
    rows = []
    for row in fst_row:
        rows.append(row.text)

    # making the dictionary
    total_assets = rows[1]

    total_assets = clear_number(total_assets)
    date = rows[0].replace('-', '/')
    total_assets = {'total_assets': total_assets, 'date': date}
    return total_assets


def filter_revenueTTMandNetIncome(html: str) -> list[dict, dict]:

    # Revenue and netIncome TTM

    soup = BeautifulSoup(html, 'html.parser')

    tables = soup.find("table", class_="table")
    # stands for the first table and body
    body = tables.tbody

    cells = body.find_all("td")
    rows = []
    for cell in cells:
        rows.append(cell.text)
    date = rows[0].replace('-', '/')

    revenueTTM = rows[1]
    net_incomeTTM = rows[2]

    revenueTTM = clear_number(revenueTTM)
    net_incomeTTM = clear_number(net_incomeTTM)

    revenueTTM = {'revenueTTM': revenueTTM, 'date': date}
    net_incomeTTM = {'net_incomeTTM': net_incomeTTM, 'date': date}
    return revenueTTM, net_incomeTTM


def filter_total_assets(html) -> dict:
    # Total Assets
    soup = BeautifulSoup(html, 'html.parser')
    tables = soup.find_all("table", class_="historical_data_table table")
    # stands for the fist table which contains date and total assets
    total_assets_quarterly = tables[1]

    fst_row = total_assets_quarterly.find_all("td")
    rows = []
    for row in fst_row:
        rows.append(row.text)

    # making the dictionary
    total_assets = rows[1]

    total_assets = clear_number(total_assets)
    date = rows[0].replace('-', '/')
    total_assets = {'total_assets': total_assets, 'date': date}
    return total_assets


def scraper(symbol: str, stock_name: str, scrap_delay: float):
    htmls = []

    # Webdriver Settings
    options = ChromeOptions()
    # Sesion without UI

    # # Driver sesion initialization
    driver = Chrome()
    driver.set_page_load_timeout(scrap_delay)

    # Revenue TTM; Expenses TTM; Net Income TTM; Num Shares; SG&A
    URL = f"https://www.macrotrends.net/stocks/charts/{symbol}/{stock_name}/income-statement?freq=Q"
    try:
        driver.get(URL)
    except Exception:
        # this is an controlled situation due to macrotrends infinite loading
        pass
    html = driver.page_source
    htmls.append(html)

    # total assets
    URL = f"https://www.macrotrends.net/stocks/charts/{symbol}/{stock_name}/total-assets"
    try:
        driver.get(URL)
    except Exception:
        pass
    html = driver.page_source
    htmls.append(html)

    # net_income and revenue (TTM)
    URL = f"https://www.macrotrends.net/stocks/charts/{symbol}/{stock_name}/net-profit-margin"

    try:
        driver.get(URL)
    except Exception:
        pass
    html = driver.page_source
    htmls.append(html)
    driver.quit()

    operating_expenses = filter_operating_expenses(htmls[0])
    num_shares = filter_num_shares(htmls[0])
    sga = filter_selling_gen_admin(htmls[0])
    total_assets = filter_total_assets(htmls[1])
    revenueTTM, net_incomeTTM = filter_revenueTTMandNetIncome(htmls[2])

    finance_variables = {"operating_expenses": operating_expenses,
                         "num_shares": num_shares,
                         "sga": sga,
                         "total_assets": total_assets,
                         "revenueTTM": revenueTTM,
                         "net_incomeTTM": net_incomeTTM,

                         }

    print(finance_variables)
    return finance_variables


if __name__ == '__main__':
    scraper('AAPL', 'aple', 2.5)
