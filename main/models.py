from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.core.files.storage import FileSystemStorage

fs = FileSystemStorage(location='/home/ubuntu/VISULYTIX_COMPILED_TOOL')

class ImageProcessing(models.Model):
    image = models.ImageField(upload_to="tmp")
    output = models.CharField(max_length=500,blank=True)
    error = models.CharField(max_length=500, blank=True)
    user = models.ForeignKey(to=User, related_name="user", null=True, blank=True)

class Binary(models.Model):
    title = models.CharField(max_length=50)
    file = models.FileField(storage=fs)
    default = models.BooleanField()
