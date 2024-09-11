import sys
import pandas as pd
from time import sleep


def main(new_symbol, file_name):
    try:

        sleep(2)

        excel_file = pd.ExcelFile(file_name)

        if new_symbol in excel_file.sheet_names:
            # refresh
            print("already exist a tab with this name, refreshing it!")

        else:
            # first ask the user to close excel, then add tab, then re-open or ask user to re-open
            dataFrame = pd.DataFrame()
            with pd.ExcelWriter(file_name, engine='openpyxl', mode='a') as writer:
                dataFrame.to_excel(writer, sheet_name=new_symbol, index=False)
    except Exception as e:
        print(e)

    sleep(20)


if __name__ == '__main__':
    new_symbol = sys.argv[1]
    file_name = sys.argv[2]

    main(new_symbol, file_name)
