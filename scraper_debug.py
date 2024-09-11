from bs4 import BeautifulSoup
from formating_tools import clear_number


def filter_data_TTM_revenue(html: str) -> dict:
    # scraping TTM Revenue
    # DELETE WHEN NOT DEBUG!!
    with open('debug.txt', 'r') as htmlfile:
        html = htmlfile.read()
    soup = BeautifulSoup(html, 'html.parser')

    tables = soup.find_all("table", class_="table")
    # stands for the fist table which contains: TTM Revenue	TTM Operating Income	Operating Margin
    operating_margin_historical_data = tables[0]

    headers = operating_margin_historical_data.find_all("thead")
    body = operating_margin_historical_data.find("tbody")
    fst_row = body.find('tr')

    date = fst_row.find_all('td')[0].get_text()
    TTM_revenue = fst_row.find_all('td')[1].get_text()

    TTM_revenue = {'TTM_revenue': TTM_revenue, 'date': date}
    return TTM_revenue


def filter_data_income_statement() -> dict:
    # Expenses TTM; Net Income TTM; Num Shares; SG&A

    with open('Debug/debug1.txt', 'r') as htmlfile:
        html = htmlfile.read()
    soup = BeautifulSoup(html, 'html.parser')

    operating_row = soup.find("div", id="row6jqxgrid")
    # stands for the fist table which contains: TTM Revenue	TTM Operating Income	Operating Margin
    # operating_margin_historical_data = tables[0]

    # headers = operating_margin_historical_data.find_all("thead")
    # body = operating_margin_historical_data.find("tbody")
    # fst_row = body.find('tr')

    # date = fst_row.find_all('td')[0].get_text()
    # TTM_revenue = fst_row.find_all('td')[1].get_text()

    # TTM_revenue = {'TTM_revenue': TTM_revenue, 'date': date}
    # return TTM_revenue
    print(operating_row)


def main():

    # Take into acount to add the billion note!!!!
    # TTM_revenue = filter_data_TTM_revenue()
    # TTM_revenue['TTM_revenue'] = clear_number(TTM_revenue['TTM_revenue'])
    exp_netIncome_numShares_SGA = filter_data_income_statement()


if __name__ == '__main__':
    main()
