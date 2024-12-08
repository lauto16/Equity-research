from undetected_chromedriver import Chrome
from selenium.webdriver import Firefox
from selenium.webdriver import FirefoxOptions
from bs4 import BeautifulSoup
from requests import get
from datetime import datetime, timedelta
from time import sleep
from time import time


def filter_dividend(html: str) -> float:
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
    dividend_percentage = float(dividend_percentage.replace('%', ''))
    return dividend_percentage


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


def its_a_date(clave):
    try:
        datetime.strptime(clave, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def get_date(value):
    dates = [key for key in value.keys() if its_a_date(key)]
    last_four_dates = sorted(dates, key=lambda x: datetime.strptime(
        x, "%Y-%m-%d"), reverse=True)[:4]
    return last_four_dates


def get_data(var: list, id: int, TTM=False) -> float:
    var = var[id]
    dates = get_date(var)
    most_recent_date = max(dates)

    value = 0
    try:

        if TTM:
            for i in range(4):
                value += float(var[dates[i]])
            return value

        data = float(var[most_recent_date])
        return data

    except:
        return 0


def scraper(symbol: str, stock_name: str, scrap_delay: float, browser: str, tries=3) -> dict:
    varlist = []
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
    income_statement = driver.execute_script("return originalData;")
    varlist.append(income_statement)
    # total assets and liabilities
    URL = f"https://www.macrotrends.net/stocks/charts/{symbol}/{stock_name}/balance-sheet?freq=Q"
    try:
        driver.get(URL)
    except Exception:
        pass
    balance_sheet = driver.execute_script("return originalData;")
    varlist.append(balance_sheet)
    # Key financial-ratios: roi; book value; CURRENT RATIO;
    URL = f"https://www.macrotrends.net/stocks/charts/{symbol}/{stock_name}/financial-ratios?freq=Q"
    try:
        driver.get(URL)
    except Exception:
        pass
    financial_ratios = driver.execute_script("return originalData;")
    varlist.append(financial_ratios)
    # dividend percentage [3]
    URL = f"https://www.macrotrends.net/stocks/charts/{symbol}/{stock_name}/dividend-yield-history"
    try:
        driver.get(URL)
    except:
        pass
    finally:
        html = driver.page_source
        driver.quit()

    # Income Statement
    # operating_expensesTTM; num_shares; basic_shares; sgaTTM; revenueTTM; net_incomeTTM; grossprofitTTM
    operating_expensesTTM = get_data(var=varlist[0], id=6, TTM=True)
    # num shares outstanding
    num_shares = get_data(var=varlist[0], id=19, TTM=False)
    basic_shares = get_data(var=varlist[0], id=18, TTM=False)
    sgaTTM = get_data(var=varlist[0], id=4, TTM=True)
    revenueTTM = get_data(var=varlist[0], id=0, TTM=True)
    net_incomeTTM = get_data(var=varlist[0], id=15, TTM=True)
    grossprofitTTM = get_data(var=varlist[0], id=2, TTM=True)

    # balance-sheet
    # assetsTTM; liabilitiesTTM; cash_on_hand; long_term_debt
    assetsTTM = get_data(var=varlist[1], id=11, TTM=True)
    liabilitiesTTM = get_data(var=varlist[1], id=16, TTM=True)
    cash_on_hand = get_data(var=varlist[1], id=0, TTM=False)
    cash_on_handTTM = get_data(var=varlist[1], id=0, TTM=True)
    long_term_debt = get_data(var=varlist[1], id=13, TTM=False)
    long_term_debtTTM = get_data(var=varlist[1], id=13, TTM=True)

    # financial-ratios
    # roi; book_value; debt_to_equity; current_ratio
    roi = get_data(var=varlist[2], id=16)
    book_value = get_data(var=varlist[2], id=17)
    book_valueTTM = get_data(var=varlist[2], id=17, TTM=True)
    debt_to_equity = get_data(var=varlist[2], id=2)
    current_ratio = get_data(var=varlist[2], id=0)
    date = get_date(value=varlist[0][0])[0]

    # URL https://www.macrotrends.net/stocks/charts/{symbol}/{stock_name}/dividend-yield-history
    dividend_percentage = filter_dividend(html)
    # Polygon API
    stock_price = filter_stock_price(symbol)

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
                         "cash_on_handTTM": cash_on_handTTM,
                         "long_term_debt": long_term_debt,
                         "long_term_debtTTM": long_term_debtTTM,
                         "roi": roi,
                         "book_value": book_value,
                         "book_valueTTM": book_valueTTM,
                         "debt_to_equity": debt_to_equity,
                         "stock_price": stock_price,
                         "current_ratio": current_ratio,
                         "date": date
                         }
    actual_time = time()
    time_refresh = actual_time - starting_time
    if time_refresh < minimum_time:
        sleeping = minimum_time - time_refresh
        sleep(sleeping)
    return finance_variables
