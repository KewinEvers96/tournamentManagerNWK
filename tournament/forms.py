from django.forms import ModelForm
from tournament.models import Tournament

class TournamentForm(ModelForm):
    class Meta:
        model = Tournament
        fields = ['']
