from bs4 import BeautifulSoup
with open('debug.txt', 'r') as htmlfile:
    html = htmlfile.read()

soup = BeautifulSoup(html, 'html.parser')
tables = soup.find_all("table", class_="table")
print(tables.preatify())
