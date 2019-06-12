from django.shortcuts import render

# Create your views here.
from django.views.generic import View
from django.http import HttpResponse
from django.conf import settings
import os 

def img_page(request, pk):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    link = os.path.join(BASE_DIR, 'static/images/{}.PNG'.format(pk)) 
    images = []
    image_data = open(link, "rb").read()
    images.append(image_data)

    return HttpResponse(images, content_type="image/png")