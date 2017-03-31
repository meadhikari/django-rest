from django.contrib.auth.models import User, Group
import time
from rest_framework import serializers
from main.models import ImageProcessing
import envoy
import subprocess
import multiprocessing


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class ImageSerializer(serializers.ModelSerializer):
    def postExec(self,output,error,pk):
        obj = ImageProcessing.objects.get(pk=pk)
        obj.output = output
        obj.error = error
        obj.save()


    def create(self, validated_data):
        validated_data.pop('output')
        validated_data.pop('error')
        img_obj = ImageProcessing.objects.create(output="Processing...", error='', **validated_data)
        def asyncwala(onExit,popenArgs):
            def runInThread(onExit, popenArgs):
                image = validated_data['image']
                # md5 = envoy.run("md5 tmp/"+image.name).std_out
                # md5 = envoy.run("sh /home/anjani/VISULYTIX_COMPILED_TOOL/run_VISULYTIX_COMPILED_TOOL.sh /usr/local/MATLAB/MATLAB_Runtime/v91/ tmp/"+image.name)
                some_command = "sh /home/anjani/VISULYTIX_COMPILED_TOOL/run_VISULYTIX_COMPILED_TOOL.sh /usr/local/MATLAB/MATLAB_Runtime/v91/ /home/anjani/static/media/tmp/"+image.name.replace(" ","_")
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
        fields = ("id","image","output","error")
