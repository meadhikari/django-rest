from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.core.files.storage import FileSystemStorage
from .fields import UniqueBooleanField
import zipfile
import time
fs = FileSystemStorage(location='/home/ubuntu/VISULYTIX_COMPILED_TOOL')
fs = FileSystemStorage(location='/Users/Adhikari/Downloads')

class ImageProcessing(models.Model):
    image = models.ImageField(upload_to="tmp")
    output = models.CharField(max_length=500,blank=True)
    error = models.CharField(max_length=500, blank=True)
    user = models.ForeignKey(to=User, related_name="user", null=True, blank=True)

class Binary(models.Model):
    title = models.CharField(max_length=50)
    file = models.FileField(storage=fs)
    default = UniqueBooleanField()
    hash = models.CharField(max_length=50,blank=True)

    def save(self, *args, **kwargs):
        zip_file_path = '/Users/Adhikari/Downloads/'+str(self.file).replace(" ","_")
        print(zip_file_path)
        zip_ref = zipfile.ZipFile(zip_file_path, 'r')
        unique_folder_name = int(time.time())
        zip_ref.extractall('/Users/Adhikari/Downloads/'+str(self.file).replace(" ","_")+str(unique_folder_name))
        zip_ref.close()
        self.hash = unique_folder_name
        super(Binary, self).save(*args, **kwargs)

