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
        print(received_json_data)
        print(received_json_data.get('reader'))
        print(Post_rssi.objects.all())

        Post_rssi.objects.create(beaconAddress = received_json_data.get('beaconAddress'),\
                                 beaconType = received_json_data.get('beaconType'),\
                                 distance = received_json_data.get('txPower'),\
                                 hashcode = received_json_data.get('lastMionuSeen'),\
                                 ibeaconData = received_json_data.get('lastMinuSeenrssi'),\
                                 lastMinuSeen = received_json_data.get('ibeaconData'),\
                                 rssi = received_json_data.get('hashcode'),\
                                 txPower = received_json_data.get('distance'),\
                                 reader=received_json_data.get('reader'))



        # print(Post_rssi.objects.all())
        print(request)
    else:
        print(request.FILES)

    return HttpResponse("hi")