from django.db import models

# Create your models here.
class Post_rssi(models.Model):
    data = models.CharField(max_length=200)
    
    def __str__(self):
        return self.data