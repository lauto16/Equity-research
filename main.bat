@echo off
REM Ruta del entorno virtual de Python
set VENV_PATH=C:\Trabajo\Equity-Research\venv

REM Activar el entorno virtual
call %VENV_PATH%\Scripts\activate

REM Archivo con la lista de símbolos
set STOCK_FILE=stocks.txt

REM Parámetros constantes
set EXCEL_FILE=C:\Trabajo\Equity-Research\STOCK_DETAILS.xlsm
set DELAY=3
set BROWSER=C

REM Leer cada línea del archivo stocks.txt y ejecutar add_stock.py con cada símbolo
for /f %%i in (%STOCK_FILE%) do (
    py add_stock.py %%i %EXCEL_FILE% %DELAY% %BROWSER%
)

REM Desactivar el entorno virtual
deactivate