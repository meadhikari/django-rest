from django.contrib.auth.models import User, Group
import time
from rest_framework import serializers
from main.models import ImageProcessing, Binary,Profile
import envoy
import subprocess
import multiprocessing
import sys
import os
#from django.conf import settings
from rest import settings
class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'password','is_superuser')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('user', 'usage','limit')
class BinarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Binary
        fields = ('title', 'file','default')
class ImageSerializer(serializers.ModelSerializer):


    user = serializers.StringRelatedField(read_only=True)

    def create(self, validated_data):
        validated_data.pop('output')
        validated_data.pop('error')
        user = self.context['request'].user
        profile = Profile.objects.filter(user=user)[0]
        usage = profile.usage

	image = validated_data['image']
           
        img_obj = ImageProcessing.objects.create(output='Processing', error='', user=user,**validated_data)
        if profile.usage >=profile.limit:
        	output = str({"outputs": [{"img": "", "name": "", "value": ""}],
                                  "error":{"message":"Limit Exceeded. Please Contact the Administrator"}})
        else:
                output = settings.processImage("/home/ubuntu/static/media/tmp/"+image.name.replace(" ","_"),'/home/ubuntu/output_images/')
                output = output.replace("/home/ubuntu/output_images/","")
                profile.usage = profile.usage + 1
                profile.save()
        obj = ImageProcessing.objects.get(pk=img_obj.pk)
        obj.output = output
        obj.save()
        return img_obj

    class Meta:
        model = ImageProcessing
        fields = ("id","image","output","error","user")
