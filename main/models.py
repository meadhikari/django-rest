from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.core.files.storage import FileSystemStorage
from .fields import UniqueBooleanField
import zipfile
import time
from django.db.models.signals import post_save
unique_folder_name = int(time.time())
fs = FileSystemStorage(location='/home/ubuntu/VISULYTIX_COMPILED_TOOL')
#fs = FileSystemStorage(location='/home/ubuntu/')

class ImageProcessing(models.Model):
    image = models.ImageField(upload_to="tmp")
    output = models.CharField(max_length=500,blank=True)
    error = models.CharField(max_length=500, blank=True)
    user = models.ForeignKey(to=User, related_name="user", null=True, blank=True)

class Binary(models.Model):
    title = models.CharField(max_length=50)
    file = models.FileField(storage=fs)
    default = UniqueBooleanField()
    hash = models.CharField(max_length=50,blank=True,default=unique_folder_name)

def post_saveops(sender, **kwargs):
     self = kwargs.get('instance')
     zip_file_path = '/home/ubuntu/VISULYTIX_COMPILED_TOOL/'+str(self.file).replace(" ","_")
     print(zip_file_path)
     zip_ref = zipfile.ZipFile(zip_file_path, 'r')
     zip_ref.extractall('/home/ubuntu/VISULYTIX_COMPILED_TOOL/'+str(self.file).replace(" ","_")+str(unique_folder_name))
     zip_ref.close()

post_save.connect(post_saveops, sender=Binary)
 

