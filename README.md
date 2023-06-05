# BBC Football Scraper

This python module scrapes the BBC Sport Football websites to extract league tables and previous results, and stores them as pandas dataframes, as well as exporting them to csv files.

## Usage

Most of the modules functions take the `league` parameter, which is a league as used in the BBC Sport URL. The easiest way to find this is to find the standings for the league on the BBC Website, which should have a url of the form `https://www.bbc.co.uk/sport/football/[league]/table`. It is this `[league]` that should be passed as the `league` parameter. For example, the Premier League's name is `premier-league`.
