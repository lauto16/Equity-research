from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font
from time import sleep
from sys import argv
from scraper import scraper
from json import load
import os

def style_tab(stock_tab) -> None:

    basic = Font(
        name='Arial Nova Cond', size=11, italic=False, color="000000")

    bold = Font(
        name='Arial Nova Cond', size=11, bold=True, italic=False, color="000000")

    stock_tab['H5'].font = bold
    stock_tab['H7'].font = bold
    stock_tab['H18'].font = basic


def getCompanyName(symbol, companies):
    return companies.get(symbol, "Símbolo no encontrado")


def refresh(tab: str, workbook: Workbook, file_name: str, companies) -> None:
    """
    Calls the scrapper and writtes the obtained data into the Workbook 

    Args:
        tab (str): The name of the tab (Symbol)
        workbook (Workbook): The excel workbook instanciated as Workbook
        companies (JsonDict): Contains SYMBOL:COMPANY_NAME
    """

    print(f'REFRESHING {tab}')
    revenue = scraper(symbol=tab, stock_name=getCompanyName(symbol=tab, companies=companies))
    stock_tab = workbook[tab]

    stock_tab['H5'] = revenue['date']
    stock_tab['H7'] = tab
    stock_tab['H18'] = revenue['revenue']

    workbook.save(file_name)

    print(f'{tab} refreshed successfully')
    sleep(2)


def mainRun(file_name: str, directory) -> None:
    """
    Main function called when button is pressed on excel file to refresh the data
    """

    try:
        print(directory)
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
                    companies=companies, file_name=file_name)

    except Exception as e:
        print(e)
        sleep(2)
        return

    print('All stocks refreshed correctly')
    sleep(2)


if __name__ == '__main__':
    file_name = argv[1]
    directory = argv[2]
    mainRun(file_name, directory)
