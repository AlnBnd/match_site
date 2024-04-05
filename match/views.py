from django.views.generic import ListView, DetailView, TemplateView
from django.shortcuts import get_object_or_404
from .models import Match, Team, Coach, Player, Standings

class TwoTablesView(TemplateView):
    template_name = 'match/matches.html'
    
    def get_context_data(self, **kwargs):
        context = super(TwoTablesView, self).get_context_data(**kwargs)
        context['matches'] = Match.objects.filter(status='FINISHED').order_by('-date')
        context['standings'] = Standings.objects.all()
        return context
    
class TeamDetailView(DetailView):
    model = Team
    template_name = 'match/team.html'
    context_object_name = 'team' 
    slug_field = 'team_slug' 
    slug_url_kwarg = 'team_slug' 
    
    def get_context_data(self, **kwargs):
        context = super(TeamDetailView, self).get_context_data(**kwargs)
        team_id = self.get_object()
        context['coach'] = get_object_or_404(Coach, team_id=team_id)
        context['players'] = Player.objects.filter(team_id=team_id)
        return context
