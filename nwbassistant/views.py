from django.template import loader

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse

def nwbassistant(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())