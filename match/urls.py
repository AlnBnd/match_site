from django.urls import path
from .views import TeamDetailView, TwoTablesView

urlpatterns = [
    path('', TwoTablesView.as_view(), name='matches'),
    path('<slug:team_slug>/', TeamDetailView.as_view(), name='team'),
    path('teams/<slug:team_slug>/', TeamDetailView.as_view(), name='team'),
    # path('teams/', TeamListView.as_view(), name='teams'),
]
