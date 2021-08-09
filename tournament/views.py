from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views import View
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Tournament, Competitor, Participation, Match
from django.forms.widgets import DateInput

# Create your views here.

class TournamentListView(ListView):
    model = Tournament
    paginate_by = 10
    ordering = 'startDate'
    page_kwarg = 'page'

class TournamentCreateView(LoginRequiredMixin, CreateView):
    model = Tournament
    context_object_name = 'tournament'
    fields= ['name', 'maxParticipants', 'startDate', 'finishDate']
    success_url = reverse_lazy('tournament:tournaments')
 
    def post(self, request):
        competitor = Competitor.objects.get(user = request.user.id)
        tournament = Tournament(name = request.POST['name'],
                                maxParticipants = request.POST['maxParticipants'],
                                startDate = request.POST['startDate'],
                                finishDate = request.POST['finishDate'],
                                started = False,
                                finished = False,
                                organizer = competitor)
        tournament.save()
        return redirect(self.success_url)
    
    def get_form(self):
        """Took from https://stackoverflow.com/questions/46735767/django-1-11-createview-adding-datepicker-for-datefields"""
        form = super(TournamentCreateView, self).get_form()
        form.fields['startDate'].widget = DateInput(attrs={'type': 'date'})
        form.fields['finishDate'].widget = DateInput(attrs={'type': 'date'})
        return form


class TournamentDetailView(DetailView):
    model = Tournament

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        tournament = context['tournament']
        competitors = Participation.objects.filter(tournament = tournament)
        competitorsCount = tournament.competitors.count()
        matches = tournament.match_set.all()[:5]
        context['competitors'] = competitors
        context['competitorsCount'] = competitorsCount
        context['matches'] = matches

        message = self.request.session.get('message', False)
        message_successful = self.request.session.get('message_successful', False)
        if message is not False:
            context['message'] = message
            del self.request.session['message']
        
        if message_successful is not False:
            context['message_successful'] = message_successful
            del self.request.session['message_successful']

        return context

class TournamentInscriptionView(LoginRequiredMixin, View):
    
    success_url = reverse_lazy('tournament:tournaments')

    def get(self, request, pk):

        message = request.session.get('message', False)
        tournament = Tournament.objects.get(pk = pk)
        context = {'tournament_name': tournament.name,
                    'tournament_id': tournament.id}
        if message is not False:
            context['message'] = message
            del request.session['message']

        return render(request, "tournament/tournamentInscriptionConfirm.html", context= context)

    def post(self, request, pk):
        competitor = Competitor.objects.get(user = request.user.id)
        tournament = Tournament.objects.get(pk = pk)

        if tournament.competitors.count() + 1 <= tournament.maxParticipants:
            try:
                competitor = Competitor.objects.get(user_id = request.user.id)
                tournament.competitors.get(pk = competitor.id)
                request.session['message'] = 'You are alredy enrolled to this tournament'        
                return redirect(reverse("tournament:tournament_inscription", args=[pk]))
            except Competitor.DoesNotExist as e:
                tournament.competitors.add(competitor)
                tournament.save()
                return redirect(self.success_url)
               
        else:
            request.session['message'] = 'The tournament is completed full'
            return redirect(reverse("tournament:tournament_inscription", args=[pk]))

class TournamentUninscriptionView(LoginRequiredMixin, View):

    def get(self, request, pk):
        template_name = "tournament/tournamentUninscription_confirm.html"
        tournament = Tournament.objects.get(pk = pk)
        try:
            competitor = Competitor.objects.get(user_id= request.user.id)
            participation = Participation.objects.get(tournament_id = pk, competitor_id = competitor.id)
            context= {
                'tournament_name': tournament.name,
                'tournament_id' : tournament.id 
            }
            return render(request, template_name, context= context)
        except Participation.DoesNotExist as e:
            request.session['message'] = 'You are not enrolled in this tournament'
            return redirect(reverse('tournament:tournament_detail', args=[pk]))
       

    def post(self, request, pk):
        
        try:
            competitor = Competitor.objects.get(user_id = request.user.id)
            tournament = Tournament.objects.get(pk = pk)
            Participation.objects.get(tournament_id = tournament.id, competitor_id = competitor.id).delete()
            request.session['message_successful'] = 'You are successfully out of {}'.format(tournament.name)
            return redirect(reverse('tournament:tournament_detail', args = [pk]))
        except Competitor.DoesNotExist as e:
            request.session['message'] = 'Competitor does not exist UwU'
            return redirect(reverse('tournament:tournament_detail'), args= [pk])
        except Tournament.DoesNotExist as e:
            request.sessionp['message'] = 'Tournament does not exist Uwu'
            return redirect(reverse('tournament:tournaments'))
        except Participation.DoesNotExist as e:
            request.session['message'] = 'You are not enrolled in this tournament'
            return redirect(reverse('tournament:tournament_detail'), args= [pk])


class MatchListView(View):
    pass

class MatchDetailView(DetailView):
    model = Match
    context_object_name = 'match'
