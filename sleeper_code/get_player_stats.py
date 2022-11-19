import json
import requests
import pandas as pd
import os

def organize_player_stats(final_teams=None):
    file_list = []
    for root, dirs, files in os.walk("raw_data"):
        if root == 'raw_data':
            for filename in files:
                file_list.append(filename)



    player_files = [file for file in file_list if 'active_stats_week_' in file]

    final_player_stats = pd.DataFrame()

    for file in player_files:
        a = pd.read_csv('raw_data/'+file)
        final_player_stats = final_player_stats.append(a)

    final_player_stats = final_player_stats.merge(final_teams)
    final_player_stats = final_player_stats.drop_duplicates()
    final_player_stats.to_csv("prod_data/active_player_stats.csv", index=False)

    return 'player stats organized'


#active_points
def get_player_stats(league_id='', positions=[], week_start=None, week_end=None, final_teams=None):


    for week in range(week_start,week_end):
        player_stats = pd.DataFrame()

        matchups = requests.get(f'https://api.sleeper.app/v1/league/{league_id}/matchups/{week}')
        matchups = matchups.json()

        for team in matchups:
            for a,b,c in zip(positions, team['starters'], team['starters_points']):

                new_row = {'week': week, 'team': team['roster_id'], 'player_id': b, 'player_points': c, 'fantasy_position': a, 'active_flag': 1}
                player_stats = player_stats.append(new_row, ignore_index=True)

        #keep only columns we need
        player_stats = player_stats[['week', 'team', 'player_id', 'player_points', 'fantasy_position', 'active_flag']]

        #active flag for active points calculation for Fantasy Plus Minus (FPM) calculation
        player_stats = player_stats.drop_duplicates()

        player_stats.to_csv(f'raw_data/active_stats_week_{week}.csv', index=False)


    #creates prod_data/active_player_stats.csv which is used for Data Viz
    organize_player_stats(final_teams=final_teams)

    print('player stats done')
    return None


#player points not only active
'''
for week in range(10,11):

    player_stats = pd.DataFrame()

    matchups = requests.get(f'https://api.sleeper.app/v1/league/{league_id}/matchups/{week}')
    matchups = matchups.json()

    team_stats = pd.DataFrame()
    for team in matchups:

        for player_id in team['players_points']:
            #print(team['roster_id'])
            #break
    #break
            #print(player_id, matchups[0]['players_points'][i])

            new_row = {'week': week, 'team': team['roster_id'], 'player_id': player_id, 'player_points': team['players_points'][player_id]}
            player_stats = player_stats.append(new_row, ignore_index=True)
    #break
    player_stats = player_stats[['week', 'team', 'player_id', 'player_points']]
    player_stats['active_flag'] = 0
    player_stats.to_csv(f'raw_data/player_stats_week_{week}.csv', index=False)
    '''


if __name__ == '__main__':
    get_player_stats()
