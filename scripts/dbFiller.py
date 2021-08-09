import json
from datetime import date, timedelta
from tournament.models import Competitor, Tournament
from django.contrib.auth.models import User

def run():
    with open("scripts/users.json", "r") as json_doc:

        users_json = json.load(json_doc)
        
        competitors = []        

        for user in users_json:
            userCreated = User.objects.create_user(user['username'], password=user['password'])
            competitor = Competitor(name = user['name'], lastname= user['lastname'], user = userCreated)
            competitor.save()
            competitors.append(competitor)

        init_date = date.today()
        finish_date = init_date + timedelta(days = 10)
        tournament = Tournament(name="Age of Empires 2: DE Mugiwaras",
                                maxParticipants = len(competitors),
                                startDate = init_date,
                                finishDate = finish_date,
                                started = False,
                                finished = False,
                                organizer = competitors[0],
                                tournamentType = 'EL')
        tournament.save()
        for competitor in competitors:
            print('Saving competitor: {}'.format(competitor))
            tournament.competitors.add(competitor)
            tournament.save()
        