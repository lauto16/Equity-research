import sys
import openpyxl
from time import sleep
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side


def main(new_symbol, file_name):
    try:
        value = input(
            "To execute this action you need to close Excel, once you close it, type '1' and enter: ")
        while value != '1':
            value = input(
                "To execute this action you need to close Excel, once you close it, type '1' and enter: ")

        wb = openpyxl.load_workbook(file_name, keep_vba=True)

        if new_symbol not in wb.sheetnames:

            new_tab = wb.create_sheet(title=new_symbol)

            # LEFT SIDE (NOTES)
            new_tab['A1'] = 'Date'
            new_tab['B1'] = 'Qty'
            new_tab['C1'] = 'Cost per share'
            new_tab['D1'] = 'Total Cost'

            new_tab['A1'].font = Font(
                name='Arial Nova Cond', size=11, bold=True, italic=False, color="000000")
            new_tab['B1'].font = Font(
                name='Arial Nova Cond', size=11, bold=True, italic=False, color="000000")
            new_tab['C1'].font = Font(
                name='Arial Nova Cond', size=11, bold=True, italic=False, color="000000")
            new_tab['D1'].font = Font(
                name='Arial Nova Cond', size=11, bold=True, italic=False, color="000000")

            # MIDDLE (DATA)
            new_tab['G5'] = 'Last Reviewed'
            new_tab['G6'] = 'Company'
            new_tab['G7'] = 'Stock ticker'
            new_tab['G8'] = 'My Money'

            new_tab['G11'] = 'Current price'
            new_tab['G12'] = 'My average cost per share'
            new_tab['G13'] = 'Fair value of the stock'
            new_tab['G14'] = 'When to buy crazy'

            new_tab['G16'] = 'Revenue'
            new_tab['G17'] = 'Expenses'
            new_tab['G18'] = 'Net Income'
            new_tab['G19'] = 'Net Income Margin'
            new_tab['G20'] = 'PE ratio'

            new_tab['G22'] = 'Assets'
            new_tab['G23'] = 'Liabilities'
            new_tab['G24'] = 'Book Value (Share equity)'
            new_tab['G25'] = 'Current ratio'
            new_tab['G26'] = 'Debt to equity ratio'

            new_tab['G28'] = 'Market cap'
            new_tab['G29'] = 'Num shares'
            new_tab['G30'] = 'Dividend'

            # RIGHT SIDE (NOTES)
            new_tab['N5'] = 'CHECKLIST - Why should I NOT buy ?'
            new_tab['N17'] = 'CHECKLIST - Why should I buy ?'

            new_tab['N5'].font = Font(
                name='Arial Nova Cond', size=11, bold=True, italic=False, color="000000")
            new_tab['N17'].font = Font(
                name='Arial Nova Cond', size=11, bold=True, italic=False, color="000000")

        else:
            print("This symbol already exists.")

        wb.save(file_name)

    except Exception as e:
        print(e)

    print(f"Symbol {new_symbol} added correctly!")
    sleep(2)


if __name__ == '__main__':
    new_symbol = sys.argv[1]
    file_name = sys.argv[2]

    main(new_symbol, file_name)
