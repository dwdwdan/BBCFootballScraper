import requests
import pandas as pd
from tabulate import tabulate
from bs4 import BeautifulSoup

league = "premier-league"
URL = "https://www.bbc.co.uk/sport/football/" + league

def get_table(URL):
    URL = URL + "/table"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    col_headers = ["Position", "Team", "Played", "Won", "Drawn", "Lost", "For", "Against", "GD", "Points"]
    col_indices = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]


    table = pd.DataFrame(columns=col_headers)

    standings = soup.find('tbody')
    rows = standings.findAll("tr")

    for row in rows:
        cells = row.findAll("td")
        row_list = []
        for i in col_indices:
            cell = cells[i].get_text()
            row_list.append(cell)


        table.loc[len(table)] = row_list

    print(tabulate(table, headers=col_headers, showindex=False))

get_table(URL)
