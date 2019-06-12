from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
from django.views.generic import View
from django.http import HttpResponse
from django.conf import settings
import os 

@csrf_exempt
def rssi_post(request):
    if request.method == 'POST':
        print(request)
        received_json_data=json.loads(request.body)
        print(received_json_data)
    else:
        print(request.FILES)

    return HttpResponse("hi")