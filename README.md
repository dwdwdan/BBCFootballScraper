# BBC Football Scraper

This python module scrapes the BBC Sport Football websites to extract league tables and previous results, and stores them as pandas dataframes, as well as exporting them to csv files.

## Usage

Most of the modules functions take the `league` parameter, which is a league as used in the BBC Sport URL. The easiest way to find this is to find the standings for the league on the BBC Website, which should have a url of the form `https://www.bbc.co.uk/sport/football/[league]/table`. It is this `[league]` that should be passed as the `league` parameter. For example, the Premier League's name is `premier-league`.

### List of Functions

- `load_csvs(league)` loads standings and results files from the pwd. It returns them as pandas dataframes
- `print_table(table)` prints a table prettily. It is only included for convenience of displaying pandas tables
- `update_results(league, start_year, start_month, end_year, end_month)` scrapes the BBC Website to get all results between the start date and end date. I do not know what happens if future dates are included if they contain unplayed matches - at the time of writing there is no scheduled matches.
- `update_table(league)` scrapes the BBC Website to get the current standings. I believe this will break during the football season, due to an additional column being present (change), though this is only a few numbers to change in the code to adapt.
