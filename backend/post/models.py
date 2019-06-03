from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.title


class Bachelor_data(models.Model):
    number = models.IntegerField()
    data = models.TextField()

    def __str__(self):
        return str(self.number)

class IoT_data(models.Model):
    state = models.IntegerField()

    def __str__(self):
        return str(self.state)
    
class IoT_home(models.Model):
    time = models.IntegerField()
    temperature = models.IntegerField()
    humidity = models.IntegerField()

    def __str__(self):
        return str(self.time)