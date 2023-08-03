from django.db import models


class IPSpace(models.Model):
    ip_space = models.CharField(max_length=50, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.ip_space

