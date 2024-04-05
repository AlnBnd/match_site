from django.db import models
from django.urls import reverse
from django.utils.text import slugify

class Team(models.Model):
    team_id = models.IntegerField(primary_key=True, unique=True)
    name_team = models.CharField(max_length=25, default='Unknown', verbose_name='Название команды')
    short_name = models.CharField(max_length=10, verbose_name='Сокращённое название')
    tla = models.CharField(max_length=10, verbose_name='Аббревиатура')
    logo = models.ImageField(upload_to='team_logos/', null=True, blank=True, default='default_logo.png', verbose_name='Лого')
    team_slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name_team  

    def save(self, *args, **kwargs):
        self.team_slug = slugify(self.short_name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('team', kwargs={'team_slug': self.team_slug})
    
class CommonInfoPerson(models.Model):
    name= models.CharField(max_length=25, editable=False, default='Unknown') 
    name_team = models.CharField(max_length=25, editable=False, default='Unknown')
    date_of_birth = models.DateField(verbose_name='Дата рождения', null=True, blank=True)
    nationality = models.CharField(max_length=40, editable=True, default='Unknown', verbose_name='Национальность')

    class Meta:
        abstract = True

class Coach(CommonInfoPerson):
    coach_id = models.IntegerField(primary_key=True)
    team_id = models.ForeignKey(Team, related_name='coaches', on_delete=models.PROTECT)
    contract_start = models.IntegerField(verbose_name='Начало контракта', null=True, blank=True)
    contract_end = models.IntegerField(verbose_name='Окончание контракта', null=True, blank=True)

    def __str__(self):
        return self.name

class Player(CommonInfoPerson):
    player_id = models.IntegerField(primary_key=True)
    team_id = models.ForeignKey(Team, related_name='players', on_delete=models.PROTECT)
    position = models.CharField(max_length=25, editable=False, default='Unknown', verbose_name='Позиция') 

    def __str__(self):
        return self.name
    
class Match(models.Model):
    match_id = models.IntegerField(primary_key=True)
    date = models.DateTimeField(verbose_name='Дата и время матча')
    home_team = models.ForeignKey(Team, related_name='home_team', on_delete=models.PROTECT)
    away_team = models.ForeignKey(Team, related_name='away_team', on_delete=models.PROTECT)
    home_team_name = models.CharField(max_length=25, editable=False, default='Unknown') 
    away_team_name = models.CharField(max_length=25, editable=False, default='Unknown') 
    score_home = models.PositiveIntegerField(null=True, blank=True)
    score_away = models.PositiveIntegerField(null=True, blank=True)
    logo_home =  models.ImageField(upload_to='team_logos/', blank=True, null=True)
    logo_away =  models.ImageField(upload_to='team_logos/', blank=True, null=True)
    status = models.CharField(max_length=30, verbose_name='Статус', default='Unknown') 

    class Meta:
        verbose_name = 'Матч'
        verbose_name_plural = 'Матчи'

    def __str__(self):
        return f'{self.home_team} vs {self.away_team}, {self.date}'
    
    def formatted_month(self):
        return self.date.strftime('%m')  

    def formatted_day(self):
        return self.date.strftime('%d')    
    
class Seasons(models.Model):
    id = models.IntegerField(primary_key=True)
    season =  models.CharField(max_length=25, blank=False, verbose_name='Сезон')
    start_date =  models.DateTimeField(auto_now_add=False, verbose_name='Дата старта')
    end_date = models.DateTimeField(auto_now_add=False, verbose_name='Дата окончания')
    season_slug = models.SlugField(max_length=255, unique=True, db_index=True)
    winner = models.ForeignKey(Team, related_name='winner', blank=True, null=True, on_delete=models.PROTECT)
    name_winner = models.CharField(max_length=25, editable=False, default='Unknown') 

    def __str__(self):
        return self.season

    def save(self, *args, **kwargs):
        self.season_slug = slugify(self.season)  # Автоматическое создание слага для URL
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('season', kwargs={'season_slug': self.season_slug})

class Standings(models.Model):
    season = models.ForeignKey(Seasons, related_name='seasons', blank=True, null=True, on_delete=models.PROTECT)
    team = models.ForeignKey(Team, related_name='team', blank=True, null=True, on_delete=models.PROTECT)
    name_team = models.CharField(max_length=25, editable=False, default='Unknown')
    position = models.PositiveIntegerField(null=True, blank=True)
    played_games = models.PositiveIntegerField(null=True, blank=True)
    won = models.PositiveIntegerField(null=True, blank=True)
    draw = models.PositiveIntegerField(null=True, blank=True)
    lost = models.PositiveIntegerField(null=True, blank=True)
    points = models.PositiveIntegerField(null=True, blank=True)
    goals_for = models.PositiveIntegerField(null=True, blank=True)
    goals_against = models.PositiveIntegerField(null=True, blank=True)
    goal_different = models.IntegerField(null=True, blank=True)
