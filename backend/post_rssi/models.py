from django.db import models

# Create your models here.
class Post_rssi(models.Model):
    # beaconAddress = models.CharField(max_length=200)
    # beaconType = models.CharField(max_length=200)
    # distance = models.IntegerField()
    # hashcode = models.CharField(max_length=200)
    # ibeaconData = models.CharField(max_length=200)
    # lastMinuSeen = models.IntegerField()
    # lastMinuSeenrssi = models.IntegerField()
    # txPower = models.IntegerField()
    reader = models.CharField(max_length=200)

    def __str__(self):
        return self.reader