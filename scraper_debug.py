from bs4 import BeautifulSoup
from formating_tools import clear_number


def filter_revenue_TTM() -> dict:
    # scraping TTM Revenue
    # DELETE WHEN NOT DEBUG!!
    with open('Debug/debug1.txt', 'r') as htmlfile:
        html = htmlfile.read()
    soup = BeautifulSoup(html, 'html.parser')

    cells_revenue = []
    cells_dates = []

    soup = BeautifulSoup(html, 'html.parser')
    revenue_row = soup.find("div", id="row0jqxgrid")

    for cell in revenue_row:
        cell = cell.text
        if cell:
            cells_revenue.append(cell)

    # DATES
    dates_row = soup.find("div", id="columntablejqxgrid").children
    for cell in dates_row:
        cell = cell.text
        if cell:
            cells_dates.append(cell)
    # deletes the first column, which doesn't have dates
    cells_dates.pop(0)

    # making the dictionary
    revenue = {"revenue": cells_revenue[1], "date": cells_dates[0]}
    return revenue


def filter_operating_expenses() -> dict:
    # Expenses TTM;

    with open('Debug/debug1.txt', 'r') as htmlfile:
        html = htmlfile.read()
    soup = BeautifulSoup(html, 'html.parser')

    cells_operating_expenses = []
    cells_dates = []

    operating_row = soup.find("div", id="row6jqxgrid").children
    for cell in operating_row:
        cell = cell.text
        if cell:
            cells_operating_expenses.append(cell)

    # DATES
    dates_row = soup.find("div", id="columntablejqxgrid").children
    for cell in dates_row:
        cell = cell.text
        if cell:
            cells_dates.append(cell)
    # deletes the first column, which doesn't have dates
    cells_dates.pop(0)

    # making the dictionary
    operating_expenses = {
        "operating_expenses":  cells_operating_expenses[1], "date": cells_dates[0]}
    return operating_expenses


def filter_net_income():
    # Net Income TTM
    cells_netIncome = []
    cells_dates = []

    with open('Debug/debug1.txt', 'r') as htmlfile:
        html = htmlfile.read()

    soup = BeautifulSoup(html, 'html.parser')
    Net_income = soup.find("div", id="row15jqxgrid").children
    for cell in Net_income:
        cell = cell.text
        if cell:
            cells_netIncome.append(cell)

    # DATES
    dates_row = soup.find("div", id="columntablejqxgrid").children
    for cell in dates_row:
        cell = cell.text
        if cell:
            cells_dates.append(cell)
    # deletes the first column, which doesn't have dates
    cells_dates.pop(0)

    # making the dictionary
    net_income = {
        "net_income":  cells_netIncome[1], "date": cells_dates[0]}
    return net_income


def filter_num_shares():
    # Num Shares
    cells_num_shares = []
    cells_dates = []
    with open('Debug/debug1.txt', 'r') as htmlfile:
        html = htmlfile.read()

    soup = BeautifulSoup(html, 'html.parser')
    num_shares = soup.find("div", id="row18jqxgrid").children
    for cell in num_shares:
        cell = cell.text
        if cell:
            cells_num_shares.append(cell)

    # DATES
    dates_row = soup.find("div", id="columntablejqxgrid").children
    for cell in dates_row:
        cell = cell.text
        if cell:
            cells_dates.append(cell)
    # deletes the first column, which doesn't have dates
    cells_dates.pop(0)

    # making the dictionary
    num_shares = {
        "num_shares":  cells_num_shares[1], "date": cells_dates[0]}
    return num_shares


def filter_selling_gen_admin():
    # SG&A
    cells_S_G_A = []
    cells_dates = []
    with open('Debug/debug1.txt', 'r') as htmlfile:
        html = htmlfile.read()

    soup = BeautifulSoup(html, 'html.parser')
    sga = soup.find("div", id="row4jqxgrid").children
    for cell in sga:
        cell = cell.text
        if cell:
            cells_S_G_A.append(cell)

    # DATES
    dates_row = soup.find("div", id="columntablejqxgrid").children
    for cell in dates_row:
        cell = cell.text
        if cell:
            cells_dates.append(cell)
    # deletes the first column, which doesn't have dates
    cells_dates.pop(0)

    # making the dictionary
    sga = {
        "sga":  cells_S_G_A[1], "date": cells_dates[0]}

    return sga


def filter_total_assets() -> dict:
    # Total Assets

    with open('Debug/debug2.txt', 'r') as htmlfile:
        html = htmlfile.read()
    soup = BeautifulSoup(html, 'html.parser')

    tables = soup.find_all("table", class_="historical_data_table table")
    # stands for the fist table which contains date and total assets
    total_assets_quarterly = tables[1]

    fst_row = total_assets_quarterly.children
    rows = []
    for row in fst_row:
        if row.get_text():
            rows.append(row.get_text())
    print(rows)

    # total_assets = {'total_assets': total_assets, 'date': date}
    # return total_assets


def main():

     revenue = filter_revenue_TTM()
     operating_exp = filter_operating_expenses()
     net_income = filter_net_income()
     num_shares = filter_num_shares()
     sga = filter_selling_gen_admin()
     # Take into acount to add the billion note!!!!

     revenue["revenue"] = clear_number(revenue["revenue"])
     operating_exp["operating_expenses"] = clear_number(
         operating_exp["operating_expenses"])
     net_income["net_income"] = clear_number(net_income["net_income"])
     num_shares["num_shares"] = clear_number(num_shares["num_shares"])
     sga["sga"] = clear_number(sga["sga"])

    total_assets = filter_total_assets()


if __name__ == '__main__':
    main()
