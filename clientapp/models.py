import base64
import json
import os
from pathlib import Path

from PIL.Image import Image
from django.db import models
from main.settings import STORAGE

# Create your models here.

def bg_path(bg):
    return 'clientapp/static/images/bg' + str(bg) + '.jpg'


class Status:
    START = 'START'
    BG = 'BG'
    GUIDE = 'GUIDE'
    CAM = 'CAM'
    FRAME = 'FRAME'
    LOAD = 'LOAD'
    END = 'END'

    STATUS = [
        ('START', 'Start Page'),
        # ('PIC', 'Picture Choose'),
        ('BG', 'Background Select'),
        ('GUIDE', 'Guide before camera'),
        ('CAM', 'Camera'),
        ('FRAME', 'Frame Select'),
        ('LOAD', 'Final Loading'),
        ('END', 'End')
    ]


class Cut(models.Model):
    paper_count = models.PositiveIntegerField(default=1)
    bg = models.PositiveIntegerField(default=1)
    photos = models.JSONField(encoder=json.JSONEncoder, decoder=json.JSONDecoder, default=list)
    chromas = models.JSONField(encoder=json.JSONEncoder, decoder=json.JSONDecoder, default=list)
    frame = models.CharField(max_length=5, default='black')
    status = models.CharField(max_length=5, choices=Status.STATUS, default=Status.START)

    def add_photo(self, data: bytes, order: int) -> Path:
        if not os.path.exists(STORAGE / str(self.pk)):
            os.mkdir(STORAGE / str(self.pk))

        file_path = STORAGE / str(self.pk) / (str(order) + '_origin.png')
        with open(file_path, 'wb') as f:
            f.write(base64.decodebytes(data))

        self.photos.append(str(file_path))
        self.save()

        return file_path

    def add_chroma(self, image: Image, order: int) -> Path:
        file_path = STORAGE / str(self.pk) / (str(order) + '_chroma.png')
        image.save(file_path, 'png')

        self.chromas.append(str(file_path))
        self.save()

        return file_path


# cut = Cut()
cut = None
