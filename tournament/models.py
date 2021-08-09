from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Competitor(models.Model):
    name = models.CharField(max_length= 128)
    lastname = models.CharField(max_length= 128)
    user = models.ForeignKey(User, on_delete= models.CASCADE)


    def __str__(self):
        return self.user.username

class Tournament(models.Model):

    name = models.CharField(max_length= 128)
    maxParticipants = models.IntegerField()
    startDate = models.DateField()
    finishDate = models.DateField()
    started = models.BooleanField()
    finished = models.BooleanField()

    competitors = models.ManyToManyField('Competitor', through='Participation')

    organizer = models.ForeignKey('Competitor', on_delete= models.CASCADE, related_name='organizer')

    ELIMINATION, LEAGUE = 'EL', 'LE'
    TYPE_CHOICES = (
        (ELIMINATION, 'Elimination'),
        (LEAGUE, 'League')
    )

    tournamentType = models.CharField(max_length = 2,
                                        choices = TYPE_CHOICES,
                                        default = ELIMINATION)

    def __str__(self):
        return "{}- ({} / {})".format(self.name, self.competitors.count(), self.maxParticipants, )

class Participation(models.Model):

    score = models.CharField(max_length= 16, default= 0)
    position = models.IntegerField(default= 0)

    tournament = models.ForeignKey('Tournament', on_delete= models.CASCADE)
    competitor = models.ForeignKey('Competitor', on_delete= models.CASCADE)

    def __str__(self):
        return "{}| {} | {} | {}".format(self.tournament, self.competitor, self.score, self.position)

class Match(models.Model):
 
    homeScore = models.IntegerField(null= True)
    guestScore = models.IntegerField(null = True)

    startDate = models.DateTimeField(null = True)
    started = models.BooleanField(null = True)
    finished = models.BooleanField(default= False)

    # Foreign keys
    tournament = models.ForeignKey('Tournament', on_delete=models.CASCADE)

    homeTeam = models.ForeignKey('Competitor', on_delete= models.CASCADE, related_name="home")
    guestTeam = models.ForeignKey('Competitor', on_delete= models.CASCADE, related_name="guest")


    def __str__(self):
        hScore = "-"
        gScore = "-"
        if self.homeScore is not None:
            hScore = self.homeScore
        if self.guestScore is not None:
            gScore = self.guestScore
        
        return "{} {} - {} {}".format(self.homeTeam, hScore, gScore, self.guestTeam)