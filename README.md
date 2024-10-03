**It is necessary to run the application the following:**

- Have Chrome or Firefox updated to the latest version
- Only work in the excel workbook (it should have xlsm extension)

Steps:
(This should be done only the first time)
(Don't need to do this if the usage will be through CMD)

- Open the two bash scripts and give permissions: run_refresh_stocks.bat and run_add_stock.bat which does not contain harmful
  software and are necessary for the communication between excel and the python scripts.

- Open the excel file as usually. 
- Give editing permissions at the top 
- Close it.
- Right click on the excel file and properties. 
- Check box at the bottom of the window (security): unable.

**For excecuting the commands via CMD:**

- Add an stock (or refresh it, if already exists):
    python add_stock.py symbol C:\Path\To\myExcelFile.xlsm delay

- Refresh all stocks:
    python refresh.py myExcelFileName.xlsm C:\Path\Where\ExcelFile\Is\ delay  


delay should be a floating point number, the worst your internet connection is, the higher it should be.
normally this value should be between 2.5 and 5.0

**Recomendations**
- Proven through testing it was discovered that using Firefox can increase around 50% eficiency and speed.
  There's no difference between choosing one browser over the other, just the time and computing performance, so quality of data remains the same.
  
- Because the scraping process is usually dependent on the internet connection and other factors such as computers speed,
we recommend that if an error occurs in the scraping process, you try again. In case it doesn't fix, try increasing the
delay argument value.

**Troubleshooting**

1) **Exception ignored**
   Exception ignored in: <function Chrome.__del__ at 0x0000027DDC4E8680>
    Traceback (most recent call last):
      File "C:\path\venv\Lib\site-packages\undetected_chromedriver\__init__.py", line 843, in __del__
        self.quit()
      File "C:\path\venv\Lib\site-packages\undetected_chromedriver\__init__.py", line 798, in quit
        time.sleep(0.1)
    OSError: [WinError 6] The handle is invalid

    This error can be ignored, it's caused and ignored by undetected_chromedriver, although if you want you can change it you can do it by modifying the following line
    in the __init__.py file from undetected_chromedriver library ("C:\path\venv\Lib\site-packages\undetected_chromedriver\__init__.py")
    
    shutil.rmtree(self.user_data_dir, ignore_errors=False)
    
    change it to:
    
    shutil.rmtree(self.user_data_dir, ignore_errors=True)

3) **Permission denied**
   [Errno 13] Permission denied: 'C:\\path\\STOCK_DETAILS.xlsm'
     It occurs when you forget to close the Excel file before executing the action.

4) **'NoneType' object has no attribute 'children'** or **timeout: Timed out receiving message from renderer: 1.500** or **list index out of range**
      Message: timeout: Timed out receiving message from renderer: 1.500
      (Session info: chrome=129.0.6668.71)
    Stacktrace:
            GetHandleVerifier [0x002C6AB3+25587]
            (No symbol) [0x00259C54]
            (No symbol) [0x00152113]
            (No symbol) [0x0013E305]
            (No symbol) [0x0013E038]
            (No symbol) [0x0013C488]
            (No symbol) [0x0013CB3D]
            (No symbol) [0x00148D0A]
            (No symbol) [0x0015D2A5]
            (No symbol) [0x00161896]
            (No symbol) [0x0013D16C]
            (No symbol) [0x0015D167]
            (No symbol) [0x001D56A4]
            (No symbol) [0x001BA936]
            (No symbol) [0x0018BA73]
            (No symbol) [0x0018C4CD]
            GetHandleVerifier [0x005A4C63+3032483]
            GetHandleVerifier [0x005F6B99+3368153]
            GetHandleVerifier [0x00358F62+624802]
            GetHandleVerifier [0x003607DC+655644]
            (No symbol) [0x0026260D]
            (No symbol) [0x0025F6D8]
            (No symbol) [0x0025F875]
            (No symbol) [0x00251CA6]
            BaseThreadInitThunk [0x7658FCC9+25]
            RtlGetAppContainerNamedObjectPath [0x773D80CE+286]
            RtlGetAppContainerNamedObjectPath [0x773D809E+238]
            (No symbol) [0x00000000]

Both of the errors (NoneType and timeout) are triggered when the program haven't got enough time to copy the html. This is almost everytime caused by low delay, try increasing the delay value

5) ** Max retries exceeded with url **
  HTTPConnectionPool(host='localhost', port=56075): Max retries exceeded with url: /session/f9a8fe0a-0beb-4a03-b32e-c57159de1b5f/source (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x0000019DC829E2D0>:       Failed to establish a new connection: [WinError 10061] A connection cannot be established because the destination computer expressly denied the connection'))

Current stock price is obtained by making an api request to "Polygon", if the number of request exceeds 5 per minute it wont allow you to access to the data.
to fix this you can wait a few minutes and try again or if you have more than 5 stock symbols, refresh all of the stocks and when the error is shown, wait a bit and refresh the remaining stocks by using
add stock / refresh stock button or command
