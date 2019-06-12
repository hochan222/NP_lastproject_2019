from django.db import models

# Create your models here.
class Post_rssi(models.Model):
    distance = models.IntegerField()

    def __str__(self):
        return self.distance