from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.core.signals import request_started
from .api import get_matches_from_api, get_coach_from_api, get_squad_from_api, get_team_from_api, get_seasons_from_api, get_winner_into_teams_from_api, get_standings_from_api
from .tasks import combined_task

api_url_season = 'https://api.football-data.org/v4/competitions/PL'
api_url_matches = 'https://api.football-data.org/v4/competitions/PL/matches?season=2023'
api_url_team = 'https://api.football-data.org/v4/competitions/PL/teams?season=2023'
api_url_standings_2023 = 'http://api.football-data.org/v4/competitions/PL/standings?season=2023'
# api_url_standings_2022 = 'http://api.football-data.org/v4/competitions/PL/standings?season=2022'

@receiver(post_migrate)
def update_database(sender, **kwargs):
    get_team_from_api(api_url_team)
    get_coach_from_api(api_url_team)
    get_squad_from_api(api_url_team)
    get_winner_into_teams_from_api(api_url_season)
    get_matches_from_api(api_url_matches)
    get_seasons_from_api(api_url_season)
    get_standings_from_api(api_url_standings_2023)
    # get_standings_from_api(api_url_standings_2022)

@receiver(request_started)
def update_data(sender, **kwargs):
    combined_task()