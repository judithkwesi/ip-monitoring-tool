from django.db import models


class IPSpace(models.Model):
    ip_space = models.CharField(max_length=50, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.ip_space
    

class SyncInterval(models.Model):
    sync_interval = models.CharField(max_length=25)

    def __str__(self):
        return self.sync_interval

