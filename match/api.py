import requests
import os
from django.utils.dateparse import parse_datetime
from .models import Match, Team, Seasons, Coach, Player, Standings

os.getenv
api_key = os.getenv('API_KEY')
headers = {'X-Auth-Token': api_key}

def get_team_from_api(api_url):
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        teams_data = response.json()
        for team in teams_data['teams']:
            name_team = team['name']
            short_name = team['shortName']
            tla = team['tla']
            logo = team['crest']

            team, _ = Team.objects.update_or_create(
                team_id = team['id'],
                defaults={
                    'name_team': name_team,
                    'short_name': short_name,
                    'tla': tla,
                    'logo': logo,
                }
            )

def get_coach_from_api(api_url):
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        teams_data = response.json()
        for team in teams_data['teams']:
            name = team['coach']['name']
            date_of_birth = parse_datetime(team['coach']['dateOfBirth'])
            nationality = team['coach']['nationality']
            contract_start = team['coach']['contract']['start']
            contract_end = team['coach']['contract']['until']
            team_id = Team.objects.get(team_id=team['id'])
           
            coach, _ = Coach.objects.update_or_create(
                coach_id = team['coach']['id'],
                defaults={
                    'name': name,
                    'team_id': team_id,
                    'name_team': team_id.name_team,
                    'date_of_birth': date_of_birth,
                    'nationality': nationality,
                    'contract_start': contract_start.split('-')[0],
                    'contract_end': contract_end.split('-')[0],
                }
            )

def get_squad_from_api(api_url):
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        teams_data = response.json()
        for team in teams_data['teams']:
            team_id = Team.objects.get(team_id=team['id'])
           
            for player in team['squad']:
                name = player['name']   
                date_of_birth = parse_datetime(str(player['dateOfBirth']))
                nationality = player['nationality']
                position = player['position']

                player, _ = Player.objects.update_or_create(
                    player_id = player['id'],
                    defaults={
                        'name': name,
                        'team_id': team_id,
                        'name_team': team_id.name_team,
                        'date_of_birth': date_of_birth,
                        'nationality': nationality,
                        'position': position,
                    }
                )

def get_winner_into_teams_from_api(api_url):
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        winner_data = response.json()
        for winner in winner_data['seasons']:
            if winner['winner'] is not None and winner['winner']['id'] is not None:
                name_team = winner['winner']['name']
                short_name = winner['winner']['shortName']
                tla = winner['winner']['tla']
                logo = winner['winner']['crest']

                winner, _ = Team.objects.update_or_create(
                    team_id = winner['winner']['id'],
                    defaults={
                        'name_team': name_team,
                        'short_name': short_name,
                        'tla': tla,
                        'logo': logo,
                    }
                )

def get_seasons_from_api(api_url): 
    response = requests.get(api_url, headers=headers)   
    if response.status_code == 200:
        seasons_data = response.json()
        for season in seasons_data['seasons']:
            start_date = parse_datetime(season['startDate'])
            end_date = parse_datetime(season['endDate'])
            
            winner = None
            name_winner = 'Unknown'

            if season['winner'] is not None and season['winner']['id'] is not None:
                winner = Team.objects.get(team_id=season['winner']['id'])
                name_winner = winner.name_team
            season, _ = Seasons.objects.update_or_create(
                id = season['id'],
                defaults={
                    'season': f'{start_date.year}/{end_date.year}',
                    'winner': winner,
                    'name_winner': name_winner,  
                }
            )


def get_matches_from_api(api_url):
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        matches_data = response.json()
        for match in matches_data['matches']:
            date = parse_datetime(match['utcDate'])
            home_team = Team.objects.get(team_id=match['homeTeam']['id'])
            away_team = Team.objects.get(team_id=match['awayTeam']['id'])
            score_home = match['score']['fullTime']['home']
            score_away = match['score']['fullTime']['away']
            status = match['status']

            match, _ = Match.objects.update_or_create(
                match_id = match['id'],
                defaults={
                    'date': date,
                    'home_team': home_team,
                    'away_team': away_team,
                    'home_team_name': home_team.name_team,  
                    'away_team_name': away_team.name_team,  
                    'score_home': score_home,
                    'score_away': score_away,
                    'logo_home': home_team.logo,
                    'logo_away': away_team.logo,
                    'status':status,
                }
            )

def get_standings_from_api(api_url):
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        standings_data = response.json()

        season_id = standings_data['season']['id']
        season, _ = Seasons.objects.update_or_create(id=season_id)

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

                st, _ = Standings.objects.get_or_create (
                    team= team,
                    season = season,
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
