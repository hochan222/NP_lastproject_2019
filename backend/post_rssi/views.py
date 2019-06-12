from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
from django.views.generic import View
from django.http import HttpResponse
from django.conf import settings

from datetime import date, time, datetime
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

import django
django.setup()

from post_rssi.models import Post_rssi

@csrf_exempt
def rssi_post(request):
    if request.method == 'POST':
        received_json_data=json.loads(request.body)
        print(received_json_data)
        Post_rssi.objects.create(reader=received_json_data)
        print(Post_rssi.objects.all())
        print(request)
    else:
        print(request.FILES)

    return HttpResponse("hi")