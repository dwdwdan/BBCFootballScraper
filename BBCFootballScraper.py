"""A module to scrape the bbc football website and extract standings and results"""


import requests
import pandas as pd
import dateparser
from os.path import isfile
from tabulate import tabulate
from bs4 import BeautifulSoup

league = "premier-league"
BASE_URL = "https://www.bbc.co.uk/sport/football/"


def load_csvs(league):
    """Load csvs previously generated.

    Inputs: league - the league the csv's correspond to

    Outputs: Standings - A pandas dataframe with the standings for the league stored in the csv
             Results - A pandas dataframe with the results from the csv"""


    if isfile(league+"-table.csv"):
        standings = pd.read_csv(league+"-table.csv")
    else:
        print("No Standings File Found for " + league)
        standings = None
    if isfile(league+"-results.csv"):
        results = pd.read_csv(league+"-results.csv")
    else:
        print("No Results File Found for " + league)
        results = None

    return standings, results


def update_table(league):
    """Update the standings in the csv. Also returns the standings as a pandas dataframe.

    Inputs: league - The league to query
    """
    URL = BASE_URL + league + "/table"
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


def __get_results_single_month(league, year, month):
    date = str(year) + "-" + f"{month:02}"
    URL = BASE_URL + league + "/scores-fixtures/" + date
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

def __get_results_single_year(league, year, months):
    col_headers = ["Date", "Home Team", "Home Score", "Away Score", "Away Team"]
    table = pd.DataFrame(columns=col_headers)
    for month in months:
        month_table = __get_results_single_month(league, year, month)
        table = pd.concat([table, month_table])

    return table

def update_results(league, start_year, start_month, end_year, end_month):
    """Update the results in the csv. Also returns the results as pandas dataframe.

    Inputs: league - the league to scrape
            start_year - The year of the first month
            start_month - The first month to consider. An integer between 1 and 12
            end_year - The year of the last month
            end_month - The last month to consider. An integer between 1 and 12
    """
    if end_year == start_year:
        months = range(start_month, end_month)
        table = __get_results_single_year(league, start_year, months)
        return table

    table = __get_results_single_year(league, start_year, range(start_month,12))

    if end_year > start_year + 2:
        for year in range(start_year + 1, end_year - 1):
            year_table = __get_results_single_year(league, year, range(1,12))
            table = pd.concat([table, year_table])

    last_year_table = __get_results_single_year(league, end_year, range(1, end_month))
    table = pd.concat([table, last_year_table])

    table.sort_values(by="Date", inplace=True)


    table.to_csv(league+"-results.csv", index=False)
    return table


def print_table(table):
    """Pretty print a table"""
    print(tabulate(table, headers='keys', showindex=False))


