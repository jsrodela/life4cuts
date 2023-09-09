from django.db import models

# Create your models here.

class Frame(models.Model):
    cut = models.ForeignKey("Cut", related_name="cut", on_delete=models.SET_NULL, null=True)

class Cut(models.Model):
    paper_count = models.PositiveIntegerField(default=1)
    bg = models.PositiveIntegerField(default=1)

