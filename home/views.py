from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from .forms import RegistrationForm
from django.urls import reverse_lazy

from django.db import IntegrityError
from tournament.models import Competitor
# Create your views here.

class RegistrationView(View):
    url_success = reverse_lazy('home:index')
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'registration/registration.html', context={"form": form})

    def post(self, request):
        form = RegistrationForm(request.POST)

        if form.is_valid():
            try:
                email = form.cleaned_data['email']
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = User.objects.create_user(username= username, email=email, password= password)
                competitor = Competitor.objects.create(name= form.cleaned_data['name'], lastname= form.cleaned_data['lastname'], user= user)
            except IntegrityError:
                form.add_error('username', 'username is already in use please use another one')
                return render(request, 'registration/registration.html', context={'form': form})

            return redirect(self.url_success)
        else:
            return render(request, 'registration/registration.html', context={"form": form})

