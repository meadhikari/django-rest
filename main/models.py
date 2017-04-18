from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class ImageProcessing(models.Model):
    image = models.ImageField(upload_to="tmp")
    output = models.CharField(max_length=500,blank=True)
    error = models.CharField(max_length=500, blank=True)
    user = models.ForeignKey(to=User, related_name="user", null=True, blank=True)

