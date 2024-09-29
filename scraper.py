from undetected_chromedriver import Chrome
from undetected_chromedriver import ChromeOptions
from bs4 import BeautifulSoup
from formating_tools import clear_number


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


def filter_total_assets(html: str) -> dict:
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


def filter_gross_profit(html: str) -> dict:
    # Gross profit
    soup = BeautifulSoup(html, 'html.parser')

    cells_gross_profit = []
    cells_dates = []

    soup = BeautifulSoup(html, 'html.parser')
    gross_profit_row = soup.find("div", id="row2jqxgrid")

    for cell in gross_profit_row:
        cell = cell.text
        if cell:
            cells_gross_profit.append(cell)

    # DATES
    dates_row = soup.find("div", id="columntablejqxgrid").children
    for cell in dates_row:
        cell = cell.text
        if cell:
            cells_dates.append(cell)
    # deletes the first column, which doesn't have dates
    cells_dates.pop(0)

    # making the dictionary
    gross_profitTTM = 0
    for i in range(1, 5):
        gross_profitTTM += clear_number(cells_gross_profit[i].replace('.', ''))

    date = cells_dates[0].replace('-', '/')

    gross_profitTTM = {
        'grossprofitTTM': gross_profitTTM, 'date': date}
    return gross_profitTTM


def filter_dividend(html: str) -> dict:
    # dividend Yield
    soup = BeautifulSoup(html, 'html.parser')

    paragraph = soup.find("div", id="main_content").findChildren("div")

    i = 0
    for div in paragraph:
        if i == 1:
            dividend = div.find_all("strong")
            dividend_percentage = dividend[1].text
            break
        i += 1
    dividend_percentage = dividend_percentage.replace('%', '')
    dividend_percentage = {'dividend_percentage': dividend_percentage}
    return dividend_percentage


def filter_total_liabilities(html: str) -> dict:
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


def filter_roi(html: str) -> dict:
    # Filter ROI TTM
    cells_roi = []
    cells_dates = []
    soup = BeautifulSoup(html, 'html.parser')
    roi = soup.find("div", id="row16jqxgrid").children

    for cell in roi:
        cell = cell.get_text()
        if cell:
            cells_roi.append(cell)

    # DATES
    dates_row = soup.find("div", id="columntablejqxgrid").children
    for cell in dates_row:
        cell = cell.text
        if cell:
            cells_dates.append(cell)
    # deletes the first column, which doesn't have dates
    cells_dates.pop(0)
    date = cells_dates[0].replace('-', '/')

    # making the dictionary
    roi = float(cells_roi[1])

    roi = {"roi":  roi, 'date': date}

    return roi


def filter_book_value(html: str) -> dict:
    pass


def filter_long_term_debt(html: str) -> dict:
    # LONG TERM DEBT
    cells_debt = []
    cells_dates = []
    soup = BeautifulSoup(html, 'html.parser')
    long_term_debtTTM = soup.find("div", id="row13jqxgrid").children

    for cell in long_term_debtTTM:
        cell = cell.get_text().replace('.', '')
        if cell:
            cells_debt.append(cell)

    # DATES
    dates_row = soup.find("div", id="columntablejqxgrid").children
    for cell in dates_row:
        cell = cell.text
        if cell:
            cells_dates.append(cell)
    # deletes the first column, which doesn't have dates
    cells_dates.pop(0)

    # making the dictionary
    long_term_debtTTM = 0
    for i in range(1, 5):
        long_term_debtTTM += clear_number(cells_debt[i])
    long_term_debt = clear_number(cells_debt[1])

    long_term_debtTTM = {"long_term_debtTTM":  long_term_debtTTM,
                         "long_term_debt": long_term_debt}
    return long_term_debtTTM


def filter_cash_on_hand(html: str) -> dict:
    cells_cash = []
    cells_dates = []
    soup = BeautifulSoup(html, 'html.parser')
    cash_on_handTTM = soup.find("div", id="row0jqxgrid").children

    for cell in cash_on_handTTM:
        cell = cell.get_text().replace('.', '')
        if cell:
            cells_cash.append(cell)

    # DATES
    dates_row = soup.find("div", id="columntablejqxgrid").children
    for cell in dates_row:
        cell = cell.text
        if cell:
            cells_dates.append(cell)
    # deletes the first column, which doesn't have dates
    cells_dates.pop(0)

    # making the dictionary
    cash_on_handTTM = 0
    for i in range(1, 5):
        cash_on_handTTM += clear_number(cells_cash[i])
    cash_on_hand = clear_number(cells_cash[1])

    cash_on_handTTM = {"cash_on_handTTM":  cash_on_handTTM,
                       "cash_on_hand": cash_on_hand}

    return cash_on_handTTM


def scraper(symbol: str, stock_name: str, scrap_delay: float):
    htmls = []
    options = ChromeOptions()
    # # Driver sesion initialization
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)
    driver = Chrome(options=options)
    driver.set_page_load_timeout(scrap_delay)
    driver.implicitly_wait(0)

    # Revenue TTM; Expenses TTM; Net Income TTM; Num Shares; SG&A
    URL = f"https://www.macrotrends.net/stocks/charts/{symbol}/{stock_name}/income-statement?freq=Q"
    try:
        driver.get(URL)
    except Exception:
        # this is an controlled situation due to macrotrends infinite loading
        pass
    html = driver.page_source
    htmls.append(html)

    # total assets and liabilities
    URL = f"https://www.macrotrends.net/stocks/charts/{symbol}/{stock_name}/balance-sheet?freq=Q"
    try:
        driver.get(URL)
    except Exception:
        pass
    html = driver.page_source
    htmls.append(html)

    # Key financial-ratios: roi; book value; IRR; CURRENT RATIO;
    URL = f"https://www.macrotrends.net/stocks/charts/{symbol}/{stock_name}/financial-ratios?freq=Q"

    try:
        driver.get(URL)
    except Exception:
        pass
    html = driver.page_source
    htmls.append(html)

    # dividend percentage [3]
    URL = f"https://www.macrotrends.net/stocks/charts/{symbol}/{stock_name}/dividend-yield-history"

    try:
        driver.get(URL)
    except Exception:
        pass
    html = driver.page_source
    htmls.append(html)

    driver.quit()

    # URL: https://www.macrotrends.net/stocks/charts/{symbol}/{stock_name}/income-statement?freq=Q
    operating_expensesTTM = filter_operating_expenses(htmls[0])
    num_shares = filter_num_shares(htmls[0])
    sgaTTM = filter_selling_gen_admin(htmls[0])
    revenueTTM = filter_revenue(htmls[0])
    net_incomeTTM = filter_NetIncome(htmls[0])
    grossprofitTTM = filter_gross_profit(htmls[0])

    # URL https://www.macrotrends.net/stocks/charts/{symbol}/{stock_name}/balance-sheet?freq=Q
    assetsTTM = filter_total_assets(htmls[1])
    liabilitiesTTM = filter_total_liabilities(htmls[1])

    # RETORNA UN DICCIONARIO CON DOS: CASH ON HAND Y CASH ON HAND TTM
    cash_on_hand = filter_cash_on_hand(htmls[1])
    # RETORNA UN DICCIONARIO CON DOS: long_term_debtTTM Y long_term_debt quarterly
    long_term_debt = filter_long_term_debt(htmls[1])

    # DEBE SER EN OTRA URL
    roi = filter_roi(htmls[2])
    book_value = filter_book_value(htmls[2])

    # URL https://www.macrotrends.net/stocks/charts/{symbol}/{stock_name}/dividend-yield-history
    dividend_percentage = filter_dividend(htmls[3])

    finance_variables = {"operating_expensesTTM": operating_expensesTTM,
                         "num_shares": num_shares,
                         "sgaTTM": sgaTTM,
                         "assetsTTM": assetsTTM,
                         "liabilitiesTTM": liabilitiesTTM,
                         "revenueTTM": revenueTTM,
                         "net_incomeTTM": net_incomeTTM,
                         "grossprofitTTM": grossprofitTTM,
                         "dividend_percentage": dividend_percentage,
                         "cash_on_hand": cash_on_hand,
                         "long_term_debt": long_term_debt,
                         "roi": roi
                         }
    print(finance_variables)
    return finance_variables


if __name__ == '__main__':
    scraper('rop', 'roper-technologies', 5)
