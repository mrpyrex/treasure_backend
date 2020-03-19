from django.db import models

# Create your models here.


class HouseCare (models.Model):
    name = models.CharField(max_length=250)
    address = models.TextField()
    host = models.CharField(max_length=250)
    phone = models.CharField(max_length=13)

    class Meta:
        verbose_name = 'house care fellowship center'
        verbose_name_plural = 'House Care Fellowship Centers'

    def __str__(self):
        return self.name
