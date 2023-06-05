"""A module to scrape the bbc football website and extract standings and results"""


import requests
import pandas as pd
import dateparser
from tabulate import tabulate
from bs4 import BeautifulSoup

league = "premier-league"
URL = "https://www.bbc.co.uk/sport/football/" + league

standings = pd.read_csv(league+"-table.csv")
results = pd.read_csv(league+"-matches.csv")

def update_table(URL):
    """Update the standings in the csv. Also returns the standings as a pandas dataframe.

    Inputs: URL - The URL to query
    """
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

    table.to_csv(league+"-table.csv", index=False)

    return table


def __get_results_single_month(URL, year, month):
    date = str(year) + "-" + f"{month:02}"
    URL = URL + "/scores-fixtures/" + date
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    col_headers = ["Date", "Home Team", "Home Score", "Away Score", "Away Team"]
    table = pd.DataFrame(columns=col_headers)

    match_days = soup.findAll('div', 'qa-match-block')
    for match_day in match_days:
        date_raw = match_day.find('h3').get_text()
        date= dateparser.parse(date_raw).replace(year = year).date()

        matches = match_day.findAll('li')
        for match in matches:
            home_team = match.find('span', 'sp-c-fixture__team--home')
            home_team_name = home_team.find('span', 'qa-full-team-name').get_text()
            home_team_score = home_team.find('span', 'sp-c-fixture__number').get_text()

            away_team = match.find('span', 'sp-c-fixture__team--away')
            away_team_name = away_team.find('span', 'qa-full-team-name').get_text()
            away_team_score = away_team.find('span', 'sp-c-fixture__number').get_text()
            new_row = [date, home_team_name, home_team_score, away_team_score, away_team_name]
            table.loc[len(table)] = new_row

    return table

def __get_results_single_year(URL, year, months):
    col_headers = ["Date", "Home Team", "Home Score", "Away Score", "Away Team"]
    table = pd.DataFrame(columns=col_headers)
    for month in months:
        month_table = __get_results_single_month(URL, year, month)
        table = pd.concat([table, month_table])

    return table

def update_results(URL, start_year, start_month, end_year, end_month):
    """Update the results in the csv. Also returns the results as pandas dataframe.

    Inputs: URL - the URL to scrape
            start_year - The year of the first month
            start_month - The first month to consider. An integer between 1 and 12
            end_year - The year of the last month
            end_month - The last month to consider. An integer between 1 and 12
    """
    if end_year == start_year:
        print("Start Year is the same as end year")
        months = range(start_month, end_month)
        table = __get_results_single_year(URL, start_year, months)
        return table

    print("First Year Data")
    table = __get_results_single_year(URL, start_year, range(start_month,12))
    print("Table has " + str(len(table)) + " entries")

    if end_year > start_year + 2:
        for year in range(start_year + 1, end_year - 1):
            print("Data for " + str(year))
            year_table = __get_results_single_year(URL, year, range(1,12))
            table = pd.concat([table, year_table])
            print("Table has " + str(len(table)) + " entries")

    print("Last Year Data")
    last_year_table = __get_results_single_year(URL, end_year, range(1, end_month))
    table = pd.concat([table, last_year_table])
    print("Table has " + str(len(table)) + " entries")

    print("Sorting Data")
    table.sort_values(by="Date", inplace=True)
    print("Table has " + str(len(table)) + " entries")


    table.to_csv(league+"-matches.csv", index=False)
    return table


def print_table(table):
    """Pretty print a table"""
    print(tabulate(table, headers='keys', showindex=False))


