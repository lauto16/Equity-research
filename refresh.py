from openpyxl import Workbook, load_workbook
from time import sleep
import time
import sys


def refresh(tab: str, workbook: Workbook) -> None:
    print(f'REFRESHING {tab}')
    sleep(1)


def mainRun(file_name: str) -> None:
    """
    Main function called when button is pressed on excel file to refresh the data
    """

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

            refresh(tab=tab, workbook=wb)

    except Exception as e:
        print(e)
        sleep(2)
        return

    print('All stocks refreshed correctly')
    sleep(2)


if __name__ == '__main__':
    file_name = sys.argv[1]
    mainRun(file_name)
