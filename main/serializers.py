from django.contrib.auth.models import User, Group
import time
from rest_framework import serializers
from main.models import ImageProcessing
import envoy
import subprocess
import multiprocessing


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

class ImageSerializer(serializers.ModelSerializer):


    user = serializers.StringRelatedField(read_only=True)

    def postExec(self,output,error,pk):
        obj = ImageProcessing.objects.get(pk=pk)
        obj.output = output.replace("\n","")
        obj.error = error
        obj.save()


    def create(self, validated_data):
        validated_data.pop('output')
        validated_data.pop('error')
        user = self.context['request'].user

        img_obj = ImageProcessing.objects.create(output="Processing...", error='', user=user,**validated_data)
        def asyncwala(onExit,popenArgs):
            def runInThread(onExit, popenArgs):
                image = validated_data['image']
                # md5 = envoy.run("md5 tmp/"+image.name).std_out
                # md5 = envoy.run("sh /home/anjani/VISULYTIX_COMPILED_TOOL/run_VISULYTIX_COMPILED_TOOL.sh /usr/local/MATLAB/MATLAB_Runtime/v91/ tmp/"+image.name)
                some_command = "sh /home/ubuntu/VISULYTIX_COMPILED_TOOL/run_VISULYTIX_COMPILED_TOOL.sh /usr/local/MATLAB/MATLAB_Runtime/v91/ /home/ubuntu/static/media/tmp/"+image.name.replace(" ","_")
                #some_command = "md5 tmp/" + image.name
                print(some_command)
                p = subprocess.Popen(some_command, stdout=subprocess.PIPE, shell=True)
                (output, err) = p.communicate()
                p_status = p.wait()
                if err:
                    error = err.replace("\n", "")
                else:
                    error = ""
                onExit(output,error,img_obj.pk)
            thread = multiprocessing.Process(target=runInThread, args=(onExit, popenArgs))
            thread.start()
        asyncwala(self.postExec,"")
        return img_obj

    class Meta:
        model = ImageProcessing
        fields = ("id","image","output","error","user")
