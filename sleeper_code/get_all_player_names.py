
import pandas as pd
import requests
import yaml

import pandas as pd


def get_all_player_names(sport='nfl'):
    players = requests.get(f'https://api.sleeper.app/v1/players/{sport}')
    players = players.json()

    player_data = pd.DataFrame()
    for player in players:
        try:
            player_name = players[player]['full_name']
        except:
            player_name = player

        try:
            player_depth_chart_position = players[player]['depth_chart_position']
        except:
            player_depth_chart_position = players[player]['position']

        new_row = {'player_id': players[player]['player_id'], 'player_name': player_name, 'player_team': players[player]['team'], 'player_position': players[player]['position'], 'player_depth_chart_position': player_depth_chart_position}
        #print(players[player]['player_id'])
        player_data = player_data.append(new_row, ignore_index=True)

    player_data.to_csv(f'prod_data/player_names.csv', index=False)

    print('all player names done')
    return None


if __name__ == '__main__':
    get_all_player_names()
