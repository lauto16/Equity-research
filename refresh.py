import time
import sys
import openpyxl


def mainRun(file_name: str) -> None:
    """
    Main function called when button is pressed on excel file to refresh the data
    """
    time.sleep(2)
    wb = openpyxl.load_workbook(file_name, keep_vba=True)
    print(wb.sheetnames)
    time.sleep(2)


if __name__ == '__main__':
    file_name = sys.argv[1]
    mainRun(file_name)
