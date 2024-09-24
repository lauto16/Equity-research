from undetected_chromedriver import Chrome
from undetected_chromedriver import ChromeOptions
from bs4 import BeautifulSoup
from formating_tools import clear_number
from selenium.common.exceptions import TimeoutException


def filter_revenue_TTM(html) -> dict:
    # Revenue TTM
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


def filter_operating_expenses(html) -> dict:
    # Expenses TTM;

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


def filter_net_income(html) -> dict:
    # Net Income TTM

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
    sga = clear_number(cells_S_G_A[1])
    # making the dictionary
    sga = {
        "sga":  sga, "date": date}

    return sga


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


def scraper(symbol: str, stock_name: str):
    htmls = []

    # Webdriver Settings
    options = ChromeOptions()
    # Sesion without UI
    # options.add_argument("--headless")

    # # Driver sesion initialization
    driver = Chrome()
    driver.set_page_load_timeout(2.5)

    # Revenue TTM; Expenses TTM; Net Income TTM; Num Shares; SG&A
    URL = f"https://www.macrotrends.net/stocks/charts/{symbol}/{stock_name}/income-statement?freq=Q"
    try:
        driver.get(URL)
    except TimeoutException:
        # this is an controlled situation due to macrotrends infinite loading
        pass
    html = driver.page_source
    htmls.append(html)

    # total assets
    URL = f"https://www.macrotrends.net/stocks/charts/{symbol}/{stock_name}/total-assets"
    try:
        driver.get(URL)
    except TimeoutException:
        pass
    html = driver.page_source
    htmls.append(html)

    driver.quit()

    revenue = filter_revenue_TTM(htmls[0])
    operating_expenses = filter_operating_expenses(htmls[0])
    net_income = filter_net_income(htmls[0])
    num_shares = filter_num_shares(htmls[0])
    sga = filter_selling_gen_admin(htmls[0])
    total_assets = filter_total_assets(htmls[1])

    finance_variables = {"revenue": revenue,
                         "operating_expenses": operating_expenses,
                         "net_income": net_income,
                         "num_shares": num_shares,
                         "sga": sga,
                         "total_assets": total_assets
                         }
    print(finance_variables)
    return finance_variables


if __name__ == '__main__':
    scraper('AAPL', 'apple')
