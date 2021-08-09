from tournament.models import Tournament, Match

def leagueMatchMaking (tournament: Tournament):
    competitors = tournament.competitors.all()
    
    for i in range(len(competitors)):
        for j in range(i + 1, len(competitors)):
            match = Match(homeTeam= competitors[i], guestTeam = competitors[j], tournament= tournament)
            print('Adding match: {}'.format(match))
            match.save()

def run():

    tournaments = Tournament.objects.all() 

    if tournaments[0].tournamentType == 'EL':
        leagueMatchMaking(tournament= tournaments[0])
    else: 
        print("Es una eliminación")

