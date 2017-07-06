from django.contrib.auth.models import User, Group
import time
from rest_framework import serializers
from main.models import ImageProcessing, Binary
import envoy
import subprocess
import multiprocessing
import sys
import os

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

class BinarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Binary
        fields = ('title', 'file','default')

class ImageSerializer(serializers.ModelSerializer):


    user = serializers.StringRelatedField(read_only=True)

    def postExec(self,output,error,pk):
        obj = ImageProcessing.objects.get(pk=pk)
        obj.output = output.replace("\n", "").strip()
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
                #application_name = str(Binary.objects.filter(default=True)[0].file.name)
                #some_command = "/bin/bash /home/ubuntu/VISULYTIX_COMPILED_TOOL/run_VISULYTIX_COMPILED_TOOL.sh /usr/local/MATLAB/MATLAB_Runtime/v91/ /home/ubuntu/static/media/tmp/"+image.name.replace(" ","_")+" "+application_name


                current_python_executable = Binary.objects.filter(default=True)[0]
                path_to_folder  = "_".join(str(Binary.objects.filter(default=True)[0].file.path).replace(".zip","").split("_")[:-1])+".zip"+current_python_executable.hash
                path_to_folder = path_to_folder+"/"
                path_to_folder = path_to_folder+ '_'.join(str(Binary.objects.filter(default=True)[0].file.name).replace(".zip","").split("_")[:-1])
                path_to_folder = path_to_folder+"/"

                #full_path = '/Users/Adhikari/Downloads/'+str(current_python_executable.file.name)+str(hash)+"."+str(current_python_executable.file.name)+"."+"dependency"
                sys.path.append(path_to_folder)
                import pegasus as p
                output = p.processImage("/home/ubuntu/static/media/tmp/"+image.name.replace(" ","_"), '/home/ubuntu/output_images/')
                '''
                some_command = "md5 tmp/" + image.name
                print(some_command)
                p = subprocess.Popen(some_command, stdout=subprocess.PIPE, shell=True)
                (output, err) = p.communicate()
                p_status = p.wait()
                if err:
                    error = err.replace("\n", "")
                else:
                    error = ""
                '''
                onExit(output,'',img_obj.pk)
                
            thread = multiprocessing.Process(target=runInThread, args=(onExit, popenArgs))
            thread.start()
        asyncwala(self.postExec,"")
        return img_obj

    class Meta:
        model = ImageProcessing
        fields = ("id","image","output","error","user")
