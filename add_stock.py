import sys
import openpyxl
from time import sleep
from openpyxl.styles import Font


def set_text(new_tab):
    """
    Sets the cell's text

    Args:
        new_tab (ExcelTab (openpyxl)): The sheet where the cell's values is going to be written

    Returns:
        None
    """

    # LEFT SIDE (NOTES)
    new_tab['A1'] = 'Date'
    new_tab['B1'] = 'Qty'
    new_tab['C1'] = 'Cost per share'
    new_tab['D1'] = 'Total Cost'

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
    new_tab['O6'] = 'Asymetric Risk - High downside, Low upside'
    new_tab['O7'] = 'Potential for technology disruption'
    new_tab['O8'] = 'Inversion - What could kill the company ?'
    new_tab['O9'] = 'High Cyclical Variation ?'
    new_tab['O10'] = 'Am I paying too high price ?'
    new_tab['O11'] = 'Is there anything I don’t know ?'

    new_tab['N17'] = 'CHECKLIST - Why should I buy ?'
    new_tab['O18'] = 'Fair Price today'
    new_tab['O19'] = 'Quality of Management, Culture, Long Tenure'
    new_tab['O20'] = 'Low Debt'
    new_tab['O21'] = 'Asymetric potential - Low downside, High upside'
    new_tab['O22'] = 'Growth Potential - scale 10x in 10yrs'
    new_tab['O23'] = 'Can it withstand a big recession ?'

    return new_tab


def add_styles(new_tab) -> None:
    """
    Addes style to excel cells

    Args:
        new_tab (ExcelTab (openpyxl)): The sheet where the styles are applied
    """
    basic = Font(
        name='Arial Nova Cond', size=11, italic=False, color="000000")

    bold = Font(
        name='Arial Nova Cond', size=11, bold=True, italic=False, color="000000")

    new_tab['A1'].font = bold
    new_tab['B1'].font = bold
    new_tab['C1'].font = bold
    new_tab['D1'].font = bold

    new_tab['N5'].font = bold
    new_tab['N17'].font = bold

    for i in range(6, 12):
        key1 = str(f'O{i}')
        key2 = str(f'O{i+12}')
        new_tab[key1].font = basic
        new_tab[key2].font = basic


def main(new_symbol: str, file_name: str) -> None:
    try:
        value = input(
            "To execute this action you need to close Excel, once you close it, type '1' and enter: ")
        while value != '1':
            value = input(
                "To execute this action you need to close Excel, once you close it, type '1' and enter: ")

        wb = openpyxl.load_workbook(file_name, keep_vba=True)

        if new_symbol not in wb.sheetnames:

            new_tab = wb.create_sheet(title=new_symbol)
            new_tab = set_text(new_tab)
            add_styles(new_tab)

        else:
            print("This symbol already exists.")

        wb.save(file_name)

    except Exception as e:
        print(e)

    print(f"Symbol {new_symbol} added correctly!")
    sleep(1.8)


if __name__ == '__main__':
    new_symbol = sys.argv[1]
    file_name = sys.argv[2]

    main(new_symbol, file_name)
