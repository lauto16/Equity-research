from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
from bs4 import BeautifulSoup

# Webdriver Settings
options = uc.ChromeOptions()
options.headless = True  # Sesion without UI
options.add_argument("--headless")

# Driver sesion initialization
driver = uc.Chrome()

# setting the sleep times to 0 when not necessary
driver.implicitly_wait(0)

URL = 'https://www.macrotrends.net/stocks/charts/WDAY/workday/operating-margin'

try:
    # Abrir la página
    driver.get(URL)

    # HTML completo
    html = driver.page_source

finally:
    try:
        driver.quit()
    except OSError as e:
        print('el error fue: ', e)
with open('./debug.txt', 'w')as debug:
    debug.write(html)
soup = BeautifulSoup(html, 'html.parser')
tables = soup.find_all("table", class_="table")
