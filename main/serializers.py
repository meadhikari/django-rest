from django.contrib.auth.models import User, Group
import time
from rest_framework import serializers
from main.models import ImageProcessing
import envoy
import subprocess


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class ImageSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        output = validated_data.pop('output')
        error = validated_data.pop('error')

        image = validated_data['image']
        #md5 = envoy.run("md5 tmp/"+image.name).std_out
        #md5 = envoy.run("sh /home/anjani/VISULYTIX_COMPILED_TOOL/run_VISULYTIX_COMPILED_TOOL.sh /usr/local/MATLAB/MATLAB_Runtime/v91/ tmp/"+image.name)
        #some_command = "sh /home/anjani/VISULYTIX_COMPILED_TOOL/run_VISULYTIX_COMPILED_TOOL.sh /usr/local/MATLAB/MATLAB_Runtime/v91/ /home/anjani/static/media/tmp/"+image.name.replace(" ","_")
        some_command = "md5 tmp/"+image.name
        print(some_command)
        p = subprocess.Popen(some_command, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()  
        p_status = p.wait()
        image = ImageProcessing.objects.create(output=output.replace("\n",""),error=err.replace("\n","") ,**validated_data)
        return image

    class Meta:
        model = ImageProcessing
        fields = ("id","image","output","error")
