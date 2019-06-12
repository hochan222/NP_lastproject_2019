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

 # beaconType = models.CharField(max_length=200)
    # distance = models.IntegerField()
    # hashcode = models.CharField(max_length=200)
    # ibeaconData = models.CharField(max_length=200)
    # lastMinuSeen = models.IntegerField()
    # lastMinuSeenrssi = models.IntegerField()
    # txPower = models.IntegerField()

@csrf_exempt
def rssi_post(request):
    if request.method == 'POST':
        Post_rssi.objects.all().delete()
        received_json_data=json.loads(request.body)
        for beacon in received_json_data.get('beacons'):
            if beacon["beaconAddress"] == "18:62:E4:3D:F7:00": 
                print("a")
            else:
                print("b")
        # print(Post_rssi.objects.all())

        Post_rssi.objects.create(data=received_json_data)

        # print(Post_rssi.objects.all())
        # print(request)
    else:
        print(request.FILES)

    return HttpResponse("hi")