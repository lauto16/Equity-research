from undetected_chromedriver import Chrome
from selenium.webdriver import Firefox
from selenium.webdriver import FirefoxOptions
from bs4 import BeautifulSoup
from utils.formating_tools import clear_number, clear_hyphen
from requests import get
from datetime import datetime, timedelta
from time import sleep
from time import time


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
        net_incomeTTM += clear_hyphen((cells_net_income[i]
                                       ).replace('$', '').replace('.', '').replace(',', '.'))
    net_income_quarterly = clear_hyphen((cells_net_income[1]
                                         ).replace('$', '').replace('.', '').replace(',', '.'))
    net_income_quarterly = net_income_quarterly / 1000
    net_incomeTTM = net_incomeTTM / 1000

    net_incomeTTM = {"net_incomeTTM": net_incomeTTM,
                     "net_income_quarterly": net_income_quarterly}
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
        operating_expensesTTM += clear_hyphen(cells_operating_expenses[i].replace(
            ',', '.').replace('$', '').replace('.', ''))/1000
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
    num_shares = clear_hyphen(cells_num_shares[1].replace('.', ''))/1000
    num_shares = {
        "num_shares": num_shares, "date": date}
    return num_shares


def filter_basic_shares(html: str) -> dict:
   # BASIC Num Shares

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
    num_shares = clear_hyphen(cells_num_shares[1].replace('.', ''))
    num_shares = {
        "basic_num_shares": num_shares, "date": date}
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
    # making sga TTM
    sgaTTM = 0
    for i in range(1, 5):
        sgaTTM += clear_hyphen(cells_S_G_A[i].replace('.',
                                                      '').replace('$', '').replace(',', '.'))/1000
    # making the dictionary
    sgaTTM = {
        "sgaTTM":  sgaTTM, "date": date}

    return sgaTTM


def filter_total_assets(html: str) -> dict:
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
    # Filter ROI
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
    roi = clear_hyphen(cells_roi[1])

    roi = {"roi":  roi, 'date': date}

    return roi


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


def filter_book_value(html: str) -> dict:
    # Filter Book Value
    cells_book_value = []
    soup = BeautifulSoup(html, 'html.parser')
    book_value = soup.find("div", id="row17jqxgrid").children

    for cell in book_value:
        cell = cell.get_text()
        if cell:
            cells_book_value.append(cell)

    # making the dictionary
    book_valueTTM = 0
    for i in range(1, 5):
        book_valueTTM += clear_hyphen(cells_book_value[i])
    book_value = clear_hyphen(cells_book_value[1])

    book_valueTTM = {"book_valueTTM":  book_valueTTM,
                     "book_value": book_value}

    return book_valueTTM


def filter_debt_to_equity(html: str) -> dict:
    # Filter Debt to Equity
    cells_debt_to_equity = []
    soup = BeautifulSoup(html, 'html.parser')
    debt_to_equity = soup.find("div", id="row2jqxgrid").children

    for cell in debt_to_equity:
        cell = cell.get_text()
        if cell:
            cells_debt_to_equity.append(cell)

    # making the dictionary
    debt_to_equity = clear_hyphen(cells_debt_to_equity[1])

    debt_to_equity = {"debt_to_equity":  debt_to_equity}

    return debt_to_equity


def filter_stock_price(symbol: str) -> dict:
    # Using polygon api
    # getting yesterday date (because it doesn't have today data)
    today = datetime.now()

    yesterday = today - timedelta(days=1)
    yesterday = yesterday.date()
    symbol = symbol.upper()
    KEY = 'ARhsHARGe4RbLut7GtYq7KDmbWChiuQC'
    r = get(
        f'https://api.polygon.io/v1/open-close/{symbol}/{str(yesterday)}?adjusted=true&apiKey={KEY}')

    if r.status_code != 200:
        yesterday = yesterday - timedelta(days=1)
        print("Unable to retrieve yesterday's stock price. Attempting to fetch the stock price from two days ago.")
        r = get(
            f'https://api.polygon.io/v1/open-close/{symbol}/{str(yesterday)}?adjusted=true&apiKey={KEY}')
        if r.status_code != 200:
            stock_price = {'stock_price': -1, 'date': '0'}
            print('There was an error, yesterday Stock price cannot be got')
            return stock_price
        print("fetch successful!")

    stock = r.json()
    stock_price = float(stock['close'])
    date = stock['from'].replace('-', '/')
    stock_price = {'stock_price': stock_price, 'date': date}
    return stock_price


def filter_current_ratio(html: str) -> dict:
    # Filter current ratio
    cells_current_ratio = []
    soup = BeautifulSoup(html, 'html.parser')
    current_ratio = soup.find("div", id="row0jqxgrid").children

    for cell in current_ratio:
        cell = cell.get_text()
        if cell:
            cells_current_ratio.append(cell)

    # making the dictionary
    current_ratio = clear_hyphen(cells_current_ratio[1])

    current_ratio = {"current_ratio":  current_ratio}

    return current_ratio


def scraper(symbol: str, stock_name: str, scrap_delay: float, browser: str, tries=3) -> dict:
    htmls = []
    minimum_time = 16
    starting_time = time()
    if browser.upper() == 'C':
        # Driver sesion initialization
        driver = Chrome()
        driver.set_page_load_timeout(scrap_delay)
        driver.implicitly_wait(0)
    elif browser.upper() == 'F':
        options = FirefoxOptions()
        # Sesion without UI
        options.add_argument('--headless')
        driver = Firefox(options=options)
        driver.set_page_load_timeout(scrap_delay)
        driver.implicitly_wait(0)

    else:
        print('Browser not valid, please chose between Chrome or Firefox')
        sleep(5)
        raise Exception('Invalid browser')

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

    # Key financial-ratios: roi; book value; CURRENT RATIO;
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
    except:
        pass
    finally:
        html = driver.page_source
        htmls.append(html)
        driver.quit()
    try:
        # URL: https://www.macrotrends.net/stocks/charts/{symbol}/{stock_name}/income-statement?freq=Q
        operating_expensesTTM = filter_operating_expenses(htmls[0])
        num_shares = filter_num_shares(htmls[0])
        basic_shares = filter_basic_shares(htmls[0])
        sgaTTM = filter_selling_gen_admin(htmls[0])
        revenueTTM = filter_revenue(htmls[0])
        net_incomeTTM = filter_NetIncome(htmls[0])
        grossprofitTTM = filter_gross_profit(htmls[0])

        # URL https://www.macrotrends.net/stocks/charts/{symbol}/{stock_name}/balance-sheet?freq=Q
        assetsTTM = filter_total_assets(htmls[1])
        liabilitiesTTM = filter_total_liabilities(htmls[1])
        cash_on_hand = filter_cash_on_hand(htmls[1])
        long_term_debt = filter_long_term_debt(htmls[1])

        # URL https://www.macrotrends.net/stocks/charts/{symbol}/{stock_name}/financial-ratios?freq=Q
        roi = filter_roi(htmls[2])
        book_value = filter_book_value(htmls[2])
        debt_to_equity = filter_debt_to_equity(htmls[2])
        current_ratio = filter_current_ratio(htmls[2])

        # URL https://www.macrotrends.net/stocks/charts/{symbol}/{stock_name}/dividend-yield-history
        dividend_percentage = filter_dividend(htmls[3])

        # Polygon API
        stock_price = filter_stock_price(symbol)
    except Exception as e:

        if tries > 0:
            print(f'there was a mistake in the load of {symbol}: ', e)
            print("trying again...")
            return scraper(symbol, stock_name, scrap_delay, browser, (tries-1))

        else:
            return

    finance_variables = {"operating_expensesTTM": operating_expensesTTM,
                         "num_shares": num_shares,
                         'basic_num_shares': basic_shares,
                         "sgaTTM": sgaTTM,
                         "assetsTTM": assetsTTM,
                         "liabilitiesTTM": liabilitiesTTM,
                         "revenueTTM": revenueTTM,
                         "net_incomeTTM": net_incomeTTM,
                         "grossprofitTTM": grossprofitTTM,
                         "dividend_percentage": dividend_percentage,
                         "cash_on_hand": cash_on_hand,
                         "long_term_debt": long_term_debt,
                         "roi": roi,
                         "book_value": book_value,
                         "debt_to_equity": debt_to_equity,
                         "stock_price": stock_price,
                         "current_ratio": current_ratio
                         }
    actual_time = time()
    time_refresh = actual_time - starting_time
    if time_refresh < minimum_time:
        sleeping = minimum_time - time_refresh
        sleep(sleeping)
    return finance_variables
