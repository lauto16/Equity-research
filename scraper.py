from undetected_chromedriver import Chrome
from undetected_chromedriver import ChromeOptions
from bs4 import BeautifulSoup
from formating_tools import clear_number
from time import sleep


def filter_revenue(html) -> dict:
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
    revenueTTM = 0
    for i in range(1, 5):
        revenueTTM += clear_number(cells_revenue[i].replace('.', ''))

    date = cells_dates[0].replace('-', '/')
    revenueTTM = {"revenueTTM": revenueTTM, "date": date}
    return revenueTTM


def filter_NetIncome(html) -> dict:
    # net TTM
    soup = BeautifulSoup(html, 'html.parser')

    cells_net_income = []

    soup = BeautifulSoup(html, 'html.parser')
    net_income_row = soup.find("div", id="row15jqxgrid")

    for cell in net_income_row:
        cell = cell.text
        if cell:
            cells_net_income.append(cell)

    # making the dictionary
    net_incomeTTM = 0
    for i in range(1, 5):
        net_incomeTTM += clear_number(cells_net_income[i])

    net_incomeTTM = {"net_incomeTTM": net_incomeTTM}
    return net_incomeTTM


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
    sgaTTM = soup.find("div", id="row4jqxgrid").children
    for cell in sgaTTM:
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
    sgaTTM = 0
    for i in range(1, 5):
        sgaTTM += clear_number(cells_S_G_A[i])

    # making the dictionary
    sgaTTM = {
        "sgaTTM":  sgaTTM, "date": date}

    return sgaTTM


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
    # Total Assets TTM
    # Total assets TTM
    cells_assets = []

    soup = BeautifulSoup(html, 'html.parser')
    assetsTTM = soup.find("div", id="row11jqxgrid").children

    for cell in assetsTTM:
        cell = cell.get_text().replace('.', '')
        if cell:
            cells_assets.append(cell)

    # making the dictionary
    assetsTTM = 0
    for i in range(1, 5):
        assetsTTM += clear_number(cells_assets[i])

    assetsTTM = {
        "assetsTTM":  assetsTTM}

    return assetsTTM


def filter_margin(html) -> dict:
    # Gross margin and TTM Gross profit
    soup = BeautifulSoup(html, 'html.parser')

    table = soup.find("table")
    # stands for the fist table which contains date and total assets
    # total_liabilities = tables[1]

    fst_row = table.find_all("td")
    rows = []
    for row in fst_row:
        rows.append(row.text)

    date = rows[0].replace('-', '/')
    grossprofitTTM = rows[2]
    gross_margin = rows[3]

    grossprofitTTM = clear_number(grossprofitTTM)

    grossprofitTTM = {
        'grossprofitTTM': grossprofitTTM, 'date': date}
    gross_margin = {
        'gross_margin': gross_margin, 'date': date}
    return grossprofitTTM, gross_margin


def filter_dividend(html) -> dict:
    # dividend Yield
    soup = BeautifulSoup(html, 'html.parser')

    paragraph = soup.find("div", id="main_content").findChildren("div")

    i = 0
    for div in paragraph:
        if i == 1:
            dividend = div.find_all("strong")
            dividend_percentile = dividend[1].text
            break
        i += 1
    dividend_percentile = dividend_percentile.replace('%', '')
    dividend_percentile = {'dividend_percentile': dividend_percentile}
    return dividend_percentile


def filter_total_liabilities(html) -> dict:
    # Total Liabilities TTM
    cells_liabilities = []

    soup = BeautifulSoup(html, 'html.parser')
    liabilitiesTTM = soup.find("div", id="row16jqxgrid").children

    for cell in liabilitiesTTM:
        cell = cell.get_text().replace('.', '')
        if cell:
            cells_liabilities.append(cell)

    # making the dictionary
    liabilitiesTTM = 0
    for i in range(1, 5):
        liabilitiesTTM += clear_number(cells_liabilities[i])

    liabilitiesTTM = {
        "liabilitiesTTM":  liabilitiesTTM}

    return liabilitiesTTM


def scraper(symbol: str, stock_name: str, scrap_delay: float):
    htmls = []

    # Webdriver Settings
    options = ChromeOptions()
    # Sesion without UI

    # # Driver sesion initialization
    driver = Chrome()
    driver.set_page_load_timeout(scrap_delay)

    # Revenue TTM; Expenses TTM; Net Income TTM; Num Shares; SG&A
    URL = f"https://www.macrotrends.net/stocks/charts/{
        symbol}/{stock_name}/income-statement?freq=Q"
    try:
        driver.get(URL)
    except Exception:
        # this is an controlled situation due to macrotrends infinite loading
        pass
    html = driver.page_source
    htmls.append(html)

    # total assets and liabilities
    URL = f"https://www.macrotrends.net/stocks/charts/{
        symbol}/{stock_name}/balance-sheet?freq=Q"
    try:
        driver.get(URL)
    except Exception:
        pass
    html = driver.page_source
    htmls.append(html)

    # Gross margin percentage and TTM Gross profit
    URL = f"https://www.macrotrends.net/stocks/charts/{
        symbol}/{stock_name}/gross-margin"

    try:
        driver.get(URL)
    except Exception:
        pass
    html = driver.page_source
    htmls.append(html)

    # dividend percentage
    URL = f"https://www.macrotrends.net/stocks/charts/{
        symbol}/{stock_name}/dividend-yield-history"

    try:
        driver.get(URL)
    except Exception:
        pass
    html = driver.page_source
    htmls.append(html)

    driver.quit()

    operating_expensesTTM = filter_operating_expenses(htmls[0])
    num_shares = filter_num_shares(htmls[0])
    sgaTTM = filter_selling_gen_admin(htmls[0])
    assetsTTM = filter_total_assets(htmls[1])  # recordar hacerlas TTM
    liabilitiesTTM = filter_total_liabilities(htmls[1])
    revenueTTM = filter_revenue(htmls[0])
    net_incomeTTM = filter_NetIncome(htmls[0])
    grossprofitTTM, gross_margin = filter_margin(htmls[2])
    dividend_percentage = filter_dividend(htmls[3])

    finance_variables = {"operating_expensesTTM": operating_expensesTTM,
                         "num_shares": num_shares,
                         "sgaTTM": sgaTTM,
                         "assetsTTM": assetsTTM,
                         "liabilitiesTTM": liabilitiesTTM,
                         "revenueTTM": revenueTTM,
                         "net_incomeTTM": net_incomeTTM,
                         "grossprofitTTM": grossprofitTTM,
                         "gross_margin": gross_margin,
                         "dividend_percentage": dividend_percentage
                         }
    print(finance_variables)
    return finance_variables


if __name__ == '__main__':
    scraper('rop', 'roper-technologies', 5)
