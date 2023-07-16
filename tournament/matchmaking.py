from django.db.models.fields.related_descriptors import ManyToManyDescriptor
from .models import Match, Tournament

class MatchMaking:

    def generate(self, tournament):
        pass

class LigueMatchMaking(MatchMaking):

    def generate(self, tournament: Tournament):

        players = tournament.competitors.all()

        for i in range(len(players)):
            for j in range(len(players)):
                match = Match(homeTeam=players[i], guestTeam = players[j], tournament= tournament)
                match.save()

class EliminationMatchMaking(MatchMaking):

    def generate(self, tournament):
        
        pass

