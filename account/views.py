from base64 import b64decode
import json

from rest_framework.generics import *
from rest_framework.permissions import *
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import *


def get_user_id_from_token(request):
    token = request.META.get('HTTP_AUTHORIZATION', None)
    token = token.replace('Token ', '')
    token = token.split('.')[1]
    user_json = json.loads(b64decode(token))
    return user_json.get('user_id')


class IsSuperUser(IsAdminUser):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class MyObtainTokenPairApi(TokenObtainPairView):
    permission_classes = AllowAny,
    serializer_class = MyTokenObtainPairSerializer


class RegisterApi(CreateAPIView):
    permission_classes = AllowAny,
    queryset = Users.objects.all()
    serializer_class = UserSerializer


class RegisterAdminApi(RegisterApi):
    permission_classes = [IsAuthenticated, IsSuperUser]
    queryset = Users.objects.all()
    serializer_class = RegisterAdminSerializer


class EditUserDataApi(RetrieveUpdateAPIView):
    permission_classes = IsAuthenticated,
    queryset = Users.objects.all()

    def put(self, request, *args, **kwargs):
        pk = get_user_id_from_token(request)
        instance = Users.objects.get(pk=pk)
        serializer = EditUserSerializer(data=request.data, instance=instance)
        serializer.is_valid()
        serializer.save()
        return Response({"changes": serializer.data})
