from django.db import models

# Create your models here.


class PrintModel(models.Model):
    img = models.FileField(upload_to='')
    cnt = models.PositiveIntegerField()
    code = models.PositiveIntegerField()
