import sys
import openpyxl
import pandas as pd
from time import sleep


def main(new_symbol, file_name):
    try:
        value = input(
            "To execute this action you need to close Excel, once you close it, type '1' and enter: ")
        while value != '1':
            value = input(
                "To execute this action you need to close Excel, once you close it, type '1' and enter: ")

        wb = openpyxl.load_workbook(file_name, keep_vba=True)

        if new_symbol not in wb.sheetnames:
            nueva_hoja = wb.create_sheet(title=new_symbol)
            nueva_hoja['A1'] = 'NEW DATA'
        else:
            print("La hoja ya existe.")

        wb.save(file_name)

    except Exception as e:
        print(e)

    sleep(20)


if __name__ == '__main__':
    new_symbol = sys.argv[1]
    file_name = sys.argv[2]

    print(f"new_symbol: {new_symbol}")
    print(f"file_name: {file_name}")

    main(new_symbol, file_name)
