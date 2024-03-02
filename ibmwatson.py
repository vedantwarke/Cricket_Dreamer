import pandas as pd
import random

ipl: pd.DataFrame = pd.read_csv(
    "IPL_Ball_by_Ball_2008_2022.csv", low_memory=False)
ipl_matches: pd.DataFrame = pd.read_csv("IPL_Matches_2008_2022.csv")
ipl_mereged_matches: pd.DataFrame = pd.merge(
    ipl, ipl_matches, how="left", on='ID')
new_ipl: pd.DataFrame = ipl_mereged_matches.drop(columns=[
    'Venue', 'BattingTeam', 'Date', 'Season',
    'Team1', 'Team2', 'TossWinner', 'TossDecision',
    'SuperOver', 'WinningTeam', 'WonBy', 'Margin', 'method',
    'Player_of_Match', 'Team1Players', 'Team2Players', 'Umpire1',
    'Umpire2'
])

batter_dataframe: pd.DataFrame = new_ipl.drop(['bowler'], axis=1)
bowler_dataframe: pd.DataFrame = new_ipl.drop(['batter'], axis=1)


def get_player_list() -> set:
    return set(batter_dataframe['batter'].unique()) | set(set(bowler_dataframe['bowler'].unique()))


def get_city_list() -> set:
    return set(new_ipl['City'].unique())


def bowler_sorted(total_player: list, location: str):
    filter_data_bowler = bowler_dataframe[bowler_dataframe['bowler'].isin(
        total_player)]
    filter_data_bowler_location = filter_data_bowler[filter_data_bowler['City'].eq(
        location)]
    final_bowler = filter_data_bowler_location.groupby(
        by=['ID', 'overs', 'bowler']).sum()[['batsman_run']]
    final_bowler_match_avg = final_bowler.groupby(by='bowler').mean()
    ye_data_1 = final_bowler_match_avg.groupby(
        by='bowler').mean()[['batsman_run']]
    return ye_data_1


def batter_sorted(total_player: list, location: str):
    filter_data_batter = batter_dataframe[batter_dataframe['batter'].isin(
        total_player)]
    filter_data_batter_location = filter_data_batter[filter_data_batter['City'].eq(
        location)]
    final_batsman = filter_data_batter_location.groupby(
        by=['ID', 'batter']).sum()[['batsman_run']]
    final_batsman_match_avg = final_batsman.groupby(by='batter').mean()
    ye_data = final_batsman_match_avg.groupby(
        by='batter').mean()[['batsman_run']]
    return ye_data
