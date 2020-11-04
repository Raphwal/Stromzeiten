from django.shortcuts import render
from .models import Generation
import csv, io



def home(request):
    context = {
        'data': Generation.objects.all().order_by('-Date')
    }
    return render(request, 'Stromzeiten_app/home.html', context)

def about(request):
    return render(request, 'Stromzeiten_app/about.html', {'title': 'About'})
# Create your views here.

