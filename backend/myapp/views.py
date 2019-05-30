from django.shortcuts import render

# Create your views here.
from django.views.generic import View
from django.http import HttpResponse
from django.conf import settings
import os 

def page(request):
    # return render(request, 'myapp/index.html')
    return render(request, 'build/index.html')
