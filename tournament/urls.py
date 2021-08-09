from django.urls import path
from .views import TournamentListView, TournamentCreateView, TournamentDetailView, TournamentInscriptionView, TournamentUninscriptionView
from .views import MatchListView, MatchDetailView

app_name = 'tournament'

urlpatterns = [
    path('tournaments', TournamentListView.as_view(), name="tournaments"),
    path('tournaments/create_tournament', TournamentCreateView.as_view(), name="create_tournament"),
    path('tournaments/<int:pk>', TournamentDetailView.as_view(), name='tournament_detail'),
    path('tournaments/<int:pk>/enroll', TournamentInscriptionView.as_view(), name='tournament_inscription'),
    path('tournaments/<int:pk>/unroll', TournamentUninscriptionView.as_view(), name= 'tournament_uninscription'),
    path('matches', MatchListView.as_view(), name="all_match_list"),
    path('matches/<int:pk>', MatchDetailView.as_view(), name="match_detail")
]
