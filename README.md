It is necessary to run the application the following: 

- Have Chrome updated to the latest version
- Only work in the excel workbook (it should have xlsm extension)

Steps:
(This should be done only the first time)

- Open the two bash scripts and give permissions: run_refresh_stocks.bat and run_add_stock.bat which does not contain harmful
  software and are necessary for the communication between excel and the python scripts.

- Open the excel file as usually. 
- Give editing permissions at the top 
- Close it.
- Right click on the excel file and properties. 
- Check box at the bottom of the window (security): unable.

For excecuting the commands via CMD:

- Add an stock:
    python add_stock.py symbol C:\Path\To\myExcelFile.xlsm delay

- Refresh all stocks:
    python refresh.py myExcelFileName.xlsm C:\Path\Where\ExcelFile\Is\ delay  


delay should be a floating point number, the worst your internet connection is, the higher it should be.
normally this value should be between 2.5 and 5.0

Because the scraping process is usually dependent on the internet connection and other factors such as computers speed,
we recommend that if an error occurs in the scraping process, you try again. In case it doesn't fix, try increasing the
delay argument value.
