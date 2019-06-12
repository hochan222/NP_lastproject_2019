from django.contrib import admin

# Register your models here.
from .models import Post_rssi, one_rssi

admin.site.register(Post_rssi)
admin.site.register(one_rssi)