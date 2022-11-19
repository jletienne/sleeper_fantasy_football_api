import json
import requests
import pandas as pd

def get_draft_id(league_id=''):

    draft = requests.get(f'https://api.sleeper.app/v1/league/{league_id}/drafts')
    draft = draft.json()

    draft_id = draft[0]['draft_id']

    return draft_id

def get_draft_results(league_id='', final_teams=None):
    draft_id = get_draft_id(league_id)

    draft = requests.get(f'https://api.sleeper.app/v1/draft/{draft_id}/picks')
    draft = draft.json()


    draft_results = pd.DataFrame()

    for pick in draft:
        new_row = {'round': pick['round'], 'round_pick': pick['draft_slot'], 'pick': pick['pick_no'], 'team': pick['roster_id'], 'player_id': pick['player_id']}
        draft_results = draft_results.append(new_row, ignore_index=True)

    draft_results = draft_results.merge(final_teams)
    draft_results.to_csv('prod_data/draft_results.csv', index=False)

    print('draft results are done')
    return None
