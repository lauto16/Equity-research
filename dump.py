from bs4 import BeautifulSoup

from formating_tools import clear_number


def filter_revenue(html) -> dict:
    # Revenue TTM
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
    revenue = clear_number(cells_revenue[1])
    date = cells_dates[0].replace('-', '/')
    revenue = {"revenue": revenue, "date": date}
    return revenue


def filter_net_income(html) -> dict:
    # Net Income TTM

    soup = BeautifulSoup(html, 'html.parser')

    cells_netIncome = []
    cells_dates = []

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
    date = cells_dates[0].replace('-', '/')
    net_income = clear_number(cells_netIncome[1])
    net_income = {
        "net_income": net_income, "date": date}
    return net_income


def main():
    sum = 21.448 + 23.636 + 33.916 + 22.956
    print(sum)


if __name__ == "__main__":
    main()
