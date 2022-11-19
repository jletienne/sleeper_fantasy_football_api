import json
import requests

def get_league_settings(league_id=''):
    league = requests.get(f'https://api.sleeper.app/v1/league/{league_id}')
    league = league.json()

    return {'playoff_week_start': league['settings']['playoff_week_start'], 'positions': [pos for pos in league['roster_positions'] if pos != 'BN']}


if __name__ == '__main__':
    get_league_settings()
