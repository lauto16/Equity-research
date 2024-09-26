from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font
from scraper import scraper
from time import sleep
from json import load
from sys import argv
import os


def style_tab(stock_tab) -> None:

    basic = Font(
        name='Arial Nova Cond', size=11, italic=False, color="000000")

    bold = Font(
        name='Arial Nova Cond', size=11, bold=True, italic=False, color="000000")

    stock_tab['H5'].font = bold
    stock_tab['H7'].font = bold

    for cell_num in range(11, 36, 1):
        stock_tab[str(f'H{cell_num}')].font = basic

    for cell_num in range(5, 36, 1):
        stock_tab[str(f'G{cell_num}')].font = basic


def getCompanyName(symbol, companies):
    return companies.get(symbol, "Símbolo no encontrado")


def refresh(tab: str, workbook: Workbook, file_name: str, companies, scrap_delay: float) -> None:
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
        symbol=tab, stock_name=getCompanyName(symbol=tab, companies=companies), scrap_delay=scrap_delay)

    stock_tab = workbook[tab]

    sleep(10)

    date = financial_values['revenueTTM']['date']
    revenueTTM = financial_values['revenueTTM']['revenueTTM']
    operating_expensesTTM = financial_values['operating_expensesTTM']['operating_expensesTTM']
    net_incomeTTM = financial_values['net_incomeTTM']['net_incomeTTM']
    net_income_margin = net_incomeTTM / revenueTTM
    num_shares = financial_values['num_shares']['num_shares']
    eps = net_incomeTTM / num_shares
    sga = financial_values['sga']['sga']
    total_assets = financial_values['total_assets']['total_assets']

    stock_tab['H5'] = date
    stock_tab['H7'] = tab

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
    # stock_tab['H23'] = pe_ratio

    # total assets
    stock_tab['H25'] = total_assets

    # num shares
    stock_tab['H32'] = num_shares

    # sga
    stock_tab['H35'] = sga

    # give styles
    style_tab(stock_tab)

    workbook.save(file_name)

    print(f'{tab} refreshed successfully')
    sleep(2)


def mainRun(file_name: str, directory, scrap_delay: float) -> None:
    """
    Main function called when button is pressed on excel file to refresh the data
    """

    try:
        json_path = os.path.join(directory, 'symbols.json')
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
                    companies=companies, file_name=file_name, scrap_delay=scrap_delay)

    except Exception as e:
        print(e)
        sleep(2)
        return

    print('All stocks refreshed correctly')
    sleep(2)


if __name__ == '__main__':

    file_name = argv[1]
    directory = argv[2]
    scrap_delay = argv[3]

    try:
        scrap_delay = float(scrap_delay)
    except:
        print(f'{scrap_delay} is not a number')
        sleep(20)

    print('Refreshing with the following options:\n')
    print(f'- file_name: {file_name}')
    print(f'- directory: {directory}')
    print(f'- scrap_delay: {scrap_delay}\n')

    try:

        mainRun(file_name, directory, scrap_delay)
    except Exception as e:
        print(e)
        sleep(20)
