
import yaml
import datetime


from sleeper_code.get_player_stats import get_player_stats
from sleeper_code.get_team_stats import get_team_stats
from sleeper_code.get_expected_wins import get_expected_wins
from sleeper_code.get_draft_results import get_draft_results
from sleeper_code.get_league_settings import get_league_settings
from sleeper_code.get_all_player_names import get_all_player_names
from sleeper_code.get_team_stats import get_team_stats
from sleeper_code.get_final_teams import get_final_teams



creds = yaml.safe_load((open('config.yaml')))

league_id = creds['league_id']

league_settings = get_league_settings(league_id=league_id)

positions = league_settings['positions']
playoff_week_start = league_settings['playoff_week_start']

sport='nfl'
year='2022'
url = f'https://sleeper.com/leagues/{league_id}/matchup'

first_thursday_of_season = datetime.datetime(2022, 9, 8) # Date of First Thursday
days_in_season_elapsed = datetime.datetime.today() - first_thursday_of_season
week_num = days_in_season_elapsed.days // 7 + 1 #pulls the week number
week_start = 1

week_end = min(week_num, playoff_week_start)

#get_all_player_names(sport=sport)

final_teams = get_final_teams(league_id=league_id)


get_player_stats(league_id=league_id, positions=positions, week_start = week_start, week_end=week_end, final_teams=final_teams)
get_team_stats(league_id=league_id, week_start = week_start, week_end=week_end, final_teams=final_teams)

get_draft_results(league_id=league_id, final_teams=final_teams)
get_expected_wins()
