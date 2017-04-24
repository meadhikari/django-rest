from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from main.serializers import UserSerializer, GroupSerializer,ImageSerializer
from main.models import ImageProcessing
from django.http import JsonResponse
from django.contrib.auth import logout

from django.contrib.auth.models import User

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class ImageProcessingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """


    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            username = self.request.query_params.get('username', None)
            if username is not None:
                queryset = ImageProcessing.objects.filter(user__username=username)
            else:
                queryset = ImageProcessing.objects.all()
        else:
            queryset = ImageProcessing.objects.filter(user=user)
        return queryset

    serializer_class = ImageSerializer


def LoginView(request):
    from django.contrib.auth import authenticate
    try:
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        return JsonResponse({'username': user.username, 'superadmin': user.is_superuser})
    except:
        return JsonResponse({'error': "Could not authenticate"})

def LogoutView(request):
    try:
        logout(request)
        return JsonResponse({'success': 'Thanks for your stay with us.'})
    except:
        return JsonResponse({'error': "Could not logout."})
