from django.contrib import admin
from tournament.models import Tournament, Competitor

# Register your models here.

class TournamentAdmin(admin.ModelAdmin):
    fields = '__all__'

class CompetitorAdmin(admin.ModelAdmin):
    fields = '__all__'

admin.site.register(Tournament)
admin.site.register(Competitor)
