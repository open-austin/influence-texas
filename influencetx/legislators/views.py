from django.shortcuts import render
from django.views.generic import DetailView, ListView

from . import models


class LegislatorListView(ListView):

    model = models.Legislator
    context_object_name = 'legislators'


class LegislatorDetailView(DetailView):

    model = models.Legislator
    context_object_name = 'legislator'
