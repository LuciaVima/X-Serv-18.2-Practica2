from django.db import models

# Create your models here.

class URL(models.Model):
    URLcorta = models.TextField()
    URLlarga = models.TextField()

