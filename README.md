For excecuting the commands via CMD:

- Add an stock:
    python add_stock.py symbol C:\Path\To\myExcelFile.xlsm delay

- Refresh all stocks:
    python refresh.py myExcelFileName.xlsm C:\Path\Where\ExcelFile\Is\ delay  


delay should be a floating point number, the worst your internet connection is, the higher it should be.
normally this value should be between 2.5 and 5.0

Because the scraping process is usually dependent on the internet connection and other factors such as computer speed,
we recommend that if an error occurs in the scraping process, you try again. In case it doesn't fix, try increasing the
delay argument value.
