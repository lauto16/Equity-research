def filter_data_TTM_revenue(html: str) -> dict:
    # scraping TTM Revenue
    # DELETE WHEN NOT DEBUG!!
    with open('debug.txt', 'r') as htmlfile:
        html = htmlfile.read()
    soup = BeautifulSoup(html, 'html.parser')

    tables = soup.find_all("table", class_="table")
    # stands for the fist table which contains: TTM Revenue	TTM Operating Income	Operating Margin
    operating_margin_historical_data = tables[0]

    body = operating_margin_historical_data.find("tbody")
    fst_row = body.find('tr')

    date = fst_row.find_all('td')[0].get_text()
    TTM_revenue = fst_row.find_all('td')[1].get_text()

    TTM_revenue = {'TTM_revenue': TTM_revenue, 'date': date}
    return TTM_revenue
