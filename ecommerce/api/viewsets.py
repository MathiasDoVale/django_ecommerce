from rest_framework import viewsets
from .serializers import UserSerializer
from user.models import CustomUser

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer