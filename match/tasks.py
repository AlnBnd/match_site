import logging
import requests
from celery import shared_task
import os
from .models import Match, Team, Standings

logger = logging.getLogger(__name__)

os.getenv
api_key = os.getenv('API_KEY')
headers = {'X-Auth-Token': api_key}

api_url_matches = 'https://api.football-data.org/v4/competitions/PL/matches?season=2023'
api_url_standings_2023 = 'http://api.football-data.org/v4/competitions/PL/standings?season=2023'

def update_matches_from_api(api_url):
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        matches_data = response.json()
        for match in matches_data['matches']:
            score_home = match['score']['fullTime']['home']
            score_away = match['score']['fullTime']['away']
            status = match['status']

            match, _ = Match.objects.update_or_create(
                match_id = match['id'],
                defaults={
                    'score_home': score_home,
                    'score_away': score_away,
                    'status':status,
                }
            )

def update_standings_from_api(api_url):
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        standings_data = response.json()

        for season_standings in standings_data['standings']:
            for st in season_standings['table']:
                team = Team.objects.get(team_id=st['team']['id'])
                position = st['position']
                played_games = st['playedGames']
                won = st['won']
                draw = st['draw']
                lost = st['lost']
                points = st['points']
                goals_for = st['goalsFor']
                goals_against = st['goalsAgainst']
                goal_different = st['goalDifference']

                st, _ = Standings.objects.update_or_create(
                    team= team,
                    defaults={ 
                        'played_games': played_games,
                        'position': position,
                        'won': won,
                        'name_team': team.name_team,
                        'draw': draw,
                        'lost': lost,
                        'points': points,
                        'goals_for': goals_for,
                        'goals_against': goals_against,
                        'goal_different': goal_different,
                    }
                )
@shared_task
def combined_task():
    try:
        update_matches_from_api(api_url_matches)
    except Exception as e:
          logger.error(f"Ошибка при получении матчей: {e}", exc_info=True)
    
    try:              
        update_standings_from_api(api_url_standings_2023)
    except Exception as e:
         logger.error(f"Ошибка при получении турнирной таблицы: {e}", exc_info=True)
