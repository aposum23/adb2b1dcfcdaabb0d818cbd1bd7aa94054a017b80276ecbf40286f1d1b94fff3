from django.db import models


class Descriptions(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=300)

class Image(models.Model):
    name = models.CharField(max_length=50)
    img = models.ImageField(upload_to='image/')
    pathIm = models.CharField(max_length=250)
