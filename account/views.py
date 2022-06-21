from base64 import b64decode
import json
from rest_framework.parsers import MultiPartParser
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.generics import *
from rest_framework.permissions import *
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import *


def get_user_id_from_token(request):
    token = request.META.get('HTTP_AUTHORIZATION', None)
    token = token.replace('Token ', '')
    token = token.split('.')[1]
    user_json = json.loads(b64decode(token+'='))
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
    parser_classes = MultiPartParser,


class RegisterAdminApi(RegisterApi):
    permission_classes = IsAuthenticated, IsSuperUser
    queryset = Users.objects.all()
    serializer_class = RegisterAdminSerializer
    parser_classes = JSONParser,


class EditUserDataApi(RetrieveUpdateAPIView):
    permission_classes = IsAuthenticated,
    queryset = Users.objects.all()

    def get(self, *args, **kwargs):
        pk = kwargs.get('pk')
        obj = Users.objects.get(pk=pk)
        res = {
            'username': obj.username,
            'first_name': obj.first_name,
            'last_name': obj.last_name,
            'email': obj.email,
            'group': obj.group,
            'ava': convert_to_txt(obj.ava.path) if obj.ava else None
        }
        return Response(res)

    def put(self, request, *args, **kwargs):
        pk = get_user_id_from_token(request)
        instance = Users.objects.get(pk=pk)
        serializer = EditUserSerializer(data=request.data, instance=instance)
        serializer.is_valid()
        serializer.save()
        obj = Users.objects.get(pk=pk)
        res = {
            'username': obj.username,
            'first_name': obj.first_name,
            'last_name': obj.last_name,
            'email': obj.email,
            'group': obj.group,
            'ava': convert_to_txt(obj.ava.path) if obj.ava else None
        }
        return Response(res)


class CreateBlogApi(CreateAPIView):
    # permission_classes = IsAdminUser,
    queryset = Blog.objects.all()
    serializer_class = CreateBlogSerializer


class UpdateBlogApi(UpdateAPIView):
    # permission_classes = IsAdminUser,
    queryset = Blog.objects.all()
    serializer_class = UpdateBlogSerializer

    def get(self, *args, **kwargs):
        pk = kwargs.get('pk')
        obj = Blog.objects.get(pk=pk)
        res = {
            'name': obj.name,
            'description': obj.description,
            'text': obj.text,
            'paralax': convert_to_txt(obj.paralax.path),
            'image': convert_to_txt(obj.image.path) if obj.image else None
        }
        return Response(res)


    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'Error': 'Method PUT not allowed'})
        try:
            instance = Blog.objects.get(pk=pk)
        except:
            return Response({'Error': 'Object does not exist'})
        serializer = UpdateBlogSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        obj = Blog.objects.get(pk=pk)
        res = {
            'name': obj.name,
            'description': obj.description,
            'text': obj.text,
            'paralax': convert_to_txt(obj.paralax.path),
            'image': convert_to_txt(obj.image.path) if obj.image else None
        }
        return Response(res)


class GetBlogsApi(APIView):
    def get(self, *args, **kwargs):
        obj = Blog.objects.all()
        res = []
        for i in obj:
            res.append({
                'id': i.pk,
                'user': i.user.username,
                'name': i.name,
                'description': i.description,
                'paralax': convert_to_txt(i.paralax.path),
            })
        return Response(res)


class GetBlogApi(APIView):
    def get(self, *args, **kwargs):
        obj = Blog.objects.get(pk=kwargs.get('pk'))
        res = {
            'user': obj.user.username,
            'name': obj.name,
            'description': obj.description,
            'paralax': convert_to_txt(obj.paralax.path),
            'image': convert_to_txt(obj.image.path) if obj.image else None
        }
        return Response(res)


class GetUserInfo(APIView):
    def get(self, *args, **kwargs):
        user = get_user_id_from_token(self.request)
        user = Users.objects.get(pk=user)
        user_data = {'username': user.username,
                'firsr_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'ava': convert_to_txt(user.ava.path) if user.ava.path else None}
        tmp = [(i.progress, i.course_tb.course_name) for i in user.user2course_set.all()]
        dct = dict((y, x) for x, y in tmp)
        user_data['courses'] = dct
        return Response(user_data)

