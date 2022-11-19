

import pandas as pd
import requests
import json
import os


def organize_team_stats(final_teams=None):

    file_list = []
    for root, dirs, files in os.walk("raw_data"):
        if root == 'raw_data':
            for filename in files:
                file_list.append(filename)



    team_files = [file for file in file_list if 'team_stats_week_' in file]

    team_stats = pd.DataFrame()

    for file in team_files:
        a = pd.read_csv('raw_data/'+file)
        team_stats = team_stats.append(a)

    team_stats = team_stats.merge(final_teams)
    team_stats = team_stats.drop_duplicates()
    team_stats.to_csv("prod_data/fantasy_team_stats.csv", index=False)

    return 'team stats organized'


def get_team_stats(league_id='', week_start = None, week_end=None, final_teams=None):

    for week in range(week_start,week_end):
        matchups = requests.get(f'https://api.sleeper.app/v1/league/{league_id}/matchups/{week}')
        matchups = matchups.json()

        team_stats = pd.DataFrame()
        for team in matchups:

            new_row = {'week': week, 'team': team['roster_id'], 'points': team['points'], 'matchup': team['matchup_id']}
            team_stats = team_stats.append(new_row, ignore_index=True)



        team_stats = team_stats[['week', 'team', 'points', 'matchup']]

        opp_stats = team_stats.copy()
        opp_stats = opp_stats.rename(columns = {'team':'opp', 'points': 'opp_points'})

        team_stats = team_stats.merge(opp_stats)
        team_stats = team_stats[team_stats['team'] != team_stats['opp']]

        #keep only columns we need
        team_stats = team_stats[['week', 'team', 'points', 'matchup', 'opp', 'opp_points']]

        #create prod data team_stats file for Data Viz
        team_stats = team_stats.drop_duplicates()
        team_stats.to_csv(f'raw_data/team_stats_week_{week}.csv', index=False)

    organize_team_stats(final_teams=final_teams)

    print('team stats are done')
    return None

if __name__ == '__main__':
    get_team_stats()
