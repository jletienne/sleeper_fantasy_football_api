import json
import requests
import pandas as pd


def get_final_teams(league_id=''):
    rosters = requests.get(f'https://api.sleeper.app/v1/league/{league_id}/rosters')
    rosters = rosters.json()

    teams = pd.DataFrame()

    for roster in rosters:
        new_row = {'user_id': roster['owner_id'], 'team': roster['roster_id']}
        teams = teams.append(new_row, ignore_index=True)


    users = requests.get(f'https://api.sleeper.app/v1/league/{league_id}/users')
    users = users.json()


    user_teams = pd.DataFrame()

    for user in users:

        try:
            team_name = user['metadata']['team_name']
        except:
            team_name = user['display_name']

        try:
            team_avatar = user['metadata']['avatar']
        except:
            team_avatar = None

        new_row = {'user_id': user['user_id'], 'user_name': user['display_name'], 'team_name': team_name, 'team_avatar': team_avatar}
        user_teams = user_teams.append(new_row, ignore_index=True)


    final_teams = teams.merge(user_teams)
    final_teams.to_csv('prod_data/final_teams.csv', index=False)
    
    return final_teams

if __name__ == '__main__':
    get_final_teams()
