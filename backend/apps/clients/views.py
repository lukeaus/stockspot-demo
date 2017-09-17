from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from .models import Client
from .permissions import IsOwner
from .serializers import ClientSerializer


class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    http_method_names = ['get', 'head', 'options']

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Client.objects.all().order_by('id')
        else:
            return Client.objects.filter(user=self.request.user).order_by('id')
