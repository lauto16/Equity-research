from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font
from scraper import scraper
from time import sleep
from json import load
from sys import argv
import os


def getCompanyName(symbol, companies):
    return companies.get(symbol, "Símbolo no encontrado")


def refresh(tab: str, workbook: Workbook, file_name: str, companies, scrap_delay: float, browser: str) -> None:
    """
    Calls the scrapper and writtes the obtained data into the Workbook 

    Args:
        tab (str): The name of the tab (Symbol)
        workbook (Workbook): The excel workbook instanciated as Workbook
        companies (JsonDict): Contains SYMBOL:COMPANY_NAME
        scrap_delay (float): Controls the number of seconds that the scraper waits
    """

    """
    
        finance_variables = {"revenue": revenue,
                         "operatin_expenses": operating_expenses,
                         "net_income": net_income,
                         "num_shares": num_shares,
                         "sga": sga
                         }

    """

    # THIS WORKS, BUT REMEMBER THAT WE NEED TTM Revenue, TTM Income and TTM Expenses, none of the three data that
    # we've been gathering about these is correct :////

    print(f'REFRESHING {tab}')
    financial_values = scraper(
        symbol=tab, stock_name=getCompanyName(symbol=tab, companies=companies), scrap_delay=scrap_delay, browser=browser)
    if financial_values is None:
        print(f'could not scrap {tab}')
        return

    stock_tab = workbook[tab]

    date = financial_values['revenueTTM']['date']
    revenueTTM = financial_values['revenueTTM']['revenueTTM']
    operating_expensesTTM = financial_values['operating_expensesTTM']['operating_expensesTTM']
    net_incomeTTM = financial_values['net_incomeTTM']['net_incomeTTM']
    # net_income_quarterly = financial_values['net_incomeTTM']['net_income_quarterly']
    num_shares = financial_values['num_shares']['num_shares']
    sgaTTM = financial_values['sgaTTM']['sgaTTM']
    assetsTTM = financial_values['assetsTTM']['assetsTTM']
    liabilitiesTTM = financial_values['liabilitiesTTM']['liabilitiesTTM']
    grossprofitTTM = financial_values['grossprofitTTM']['grossprofitTTM']
    dividend_percentage = financial_values['dividend_percentage']['dividend_percentage']
    cash_on_hand = financial_values['cash_on_hand']['cash_on_hand']
    cash_on_handTTM = financial_values['cash_on_hand']['cash_on_handTTM']
    long_term_debt = financial_values['long_term_debt']['long_term_debt']
    long_term_debtTTM = financial_values['long_term_debt']['long_term_debtTTM']
    roi = financial_values['roi']['roi']
    book_value = financial_values['book_value']['book_value']
    book_valueTTM = financial_values['book_value']['book_valueTTM']
    debt_to_equity = financial_values['debt_to_equity']['debt_to_equity']
    stock_price = financial_values['stock_price']['stock_price']
    stock_price_date = financial_values['stock_price']['date']
    basic_num_shares = financial_values['basic_num_shares']['basic_num_shares']
    current_ratio = financial_values['current_ratio']['current_ratio']

    net_income_margin = round(((net_incomeTTM * 100) / revenueTTM), 3)
    eps = net_incomeTTM / num_shares
    sga_margin = round(((sgaTTM * 100) / grossprofitTTM), 3)
    grossmarginTTM = round(((grossprofitTTM * 100) / revenueTTM), 3)
    market_cap = basic_num_shares * stock_price
    fair_value = stock_price / book_value
    pe_ratio = stock_price / eps

    stock_tab['H5'] = date
    stock_tab['H7'] = tab

    # stock price
    stock_tab['H11'] = stock_price
    # stock price date
    stock_tab['I11'] = stock_price_date

    # fair value
    stock_tab['H13'] = fair_value

    # revenue
    stock_tab['H18'] = revenueTTM

    # operating expenses
    stock_tab['H19'] = operating_expensesTTM

    # net income
    stock_tab['H20'] = net_incomeTTM

    # net income margin
    stock_tab['H21'] = net_income_margin

    # eps
    stock_tab['H22'] = eps

    # PE Ratio
    stock_tab['H23'] = pe_ratio

    # total assets
    stock_tab['H25'] = assetsTTM

    # liabilities
    stock_tab['H26'] = liabilitiesTTM

    # current ratio
    stock_tab['H28'] = current_ratio

    # market cap
    stock_tab['H31'] = market_cap

    # num shares
    stock_tab['H32'] = num_shares

    # dividend
    stock_tab['H33'] = dividend_percentage

    # free cash flow
    # stock_tab['H34'] = free_cash_flow

    # sga
    stock_tab['H35'] = sgaTTM

    # sga margin
    stock_tab['H36'] = sga_margin

    # gross profit
    stock_tab['H37'] = grossprofitTTM

    # gross margin
    stock_tab['H38'] = grossmarginTTM

    # cash on hand
    stock_tab['H39'] = cash_on_hand

    # cash on hand TTM
    stock_tab['H40'] = cash_on_handTTM

    # long term debt
    stock_tab['H41'] = long_term_debt

    # long term debt TTM
    stock_tab['H42'] = long_term_debtTTM

    # roi
    stock_tab['H43'] = roi

    # book_value
    stock_tab['H27'] = book_value

    # book_value TTM
    stock_tab['H44'] = book_valueTTM

    # debt to equity
    stock_tab['H29'] = debt_to_equity

    workbook.save(file_name)

    print(f'{tab} refreshed successfully')
    sleep(2)


def mainRun(file_name: str, directory, scrap_delay: float, browser: str) -> None:
    """
    Main function called when button is pressed on excel file to refresh the data
    """

    try:
        json_path = os.path.join(directory, 'utils/symbols.json')
        with open(json_path, 'r') as file:
            companies = load(file)
    except Exception as e:
        print(e)
        sleep(2)
        return

    try:
        print(
            "To execute this action you need to close Excel, once you close it, type '1' and enter: ")
        value = input("> ")
        while value != '1':
            print(
                "To execute this action you need to close Excel, once you close it, type '1' and enter: ")
            value = input("> ")

        wb = load_workbook(file_name, keep_vba=True)
        for tab in wb.sheetnames:
            if tab == 'SUMMARY':
                continue

            refresh(tab=tab, workbook=wb,
                    companies=companies, file_name=file_name, scrap_delay=scrap_delay, browser=browser)
    except Exception as e:
        print(e)
        sleep(10)
        return

    print('All stocks refreshed correctly')
    sleep(2)


if __name__ == '__main__':

    file_name = argv[1]
    directory = argv[2]
    scrap_delay = argv[3]
    browser = argv[4]

    if browser not in 'cCfF':
        print(
            'Browser parameter should be "c" or "C" for Chrome and "F" or "f" for Firefox')
        sleep(5)
        raise Exception

    try:
        scrap_delay = float(scrap_delay.replace(',', '.'))
    except:
        print(f'{scrap_delay} is not a number')
        sleep(20)

    print('Refreshing with the following options:\n')
    print(f'- file_name: {file_name}')
    print(f'- directory: {directory}')
    print(f'- scrap_delay: {scrap_delay}')
    print(f'- browser: {browser}\n')

    try:
        mainRun(file_name, directory, scrap_delay, browser)
    except Exception as e:
        print(e)
        sleep(20)
