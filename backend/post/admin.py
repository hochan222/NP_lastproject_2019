from django.contrib import admin

from .models import Post, Bachelor_data, IoT_data, IoT_home

admin.site.register(Post)
admin.site.register(Bachelor_data)
admin.site.register(IoT_data)
admin.site.register(IoT_home)
