from rest_framework.serializers import CharField as CF, EmailField as EF, ImageField as IM
from rest_framework.validators import UniqueValidator
from .models import Users, Blog
from edu.models import Courses, User2Course
from rest_framework.serializers import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import re


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        token['username'] = user.username
        return token


class UserSerializer(ModelSerializer):
    username = CF(
        validators=[UniqueValidator(queryset=Users.objects.all())],
        label='Username'
    )
    first_name = CF(allow_blank=True, label='First name', required=False)
    last_name = CF(allow_blank=True, label='Last name', required=False)
    email = EF(
        required=True,
        validators=[UniqueValidator(queryset=Users.objects.all())],
        label='EMail'
    )
    password = CF(min_length=8, style={'input_type': 'password'}, write_only=True, label='Password')
    confirm = CF(min_length=8, style={'input_type': 'password'}, write_only=True, label='Confirm password')
    group = CF(max_length=10, label='Group (e.g. \'1-КТ-21\' or \'2-ІП/КТ-19\')')

    class Meta:
        model = Users
        fields = 'username', 'first_name', 'last_name', 'email', 'password', 'confirm', 'group'

    def validate(self, data):
        password = data.get('password')
        confirm = data.pop('confirm')

        group = data.get('group').split(' ')[0]
        group_re = re.match(r'[1-5]-(КТ|ІП/КТ|Е|ЕП|ЕМ|ТМ)-[1-9]+[0-9]', group)
        try:
            group_re.string
        except AttributeError:
            raise ValidationError('Entered group is invalid!')

        if password != confirm:
            raise ValidationError('Entered passwords are not the same!')

        return data

    def create(self, validated_data):
        username = validated_data.get('username')
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        email = validated_data.get('email')
        group = validated_data.get('group')
        password = validated_data.get('password')

        user = Users.objects.create(username=username, first_name=first_name,
                                    last_name=last_name, email=email, group=group)
        user.set_password(password)
        if Courses.objects.all():
            for i in Courses.objects.all():
                rel = User2Course.objects.create(user_tb=user, course_tb=i)
                rel.save()
        else:
            pass
        user.save()
        return user


class EditUserSerializer(UserSerializer):
    username = CF(
        validators=[UniqueValidator(queryset=Users.objects.all())],
        label='Username', required=False
    )
    first_name = CF(allow_blank=True, label='First name', required=False)
    last_name = CF(allow_blank=True, label='Last name', required=False)
    email = EF(
        required=False,
        validators=[UniqueValidator(queryset=Users.objects.all())],
        label='EMail'
    )
    password = CF(min_length=8, style={'input_type': 'password'}, write_only=True, label='Password', required=False)
    confirm = CF(min_length=8, style={'input_type': 'password'}, write_only=True, label='Confirm password', required=False)
    group = CF(max_length=10, label='Group (e.g. \'1-КТ-21\' or \'2-ІП/КТ-19\')', required=False)

    def validate(self, data):
        if data.get('password'):
            password = data.get('password')
            confirm = data.pop('confirm')
            if password != confirm:
                raise ValidationError('Entered passwords are not the same!')
        else: pass
        if data.get('group'):
            group = data.get('group').split(' ')[0]
            group_re = re.match(r'[1-5]-(КТ|ІП/КТ|Е|ЕП|ЕМ|ТМ)-[1-9]+[0-9]', group)
            try:
                group_re.string
            except AttributeError:
                raise ValidationError('Entered group is invalid!')
        return data

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.group = validated_data.get('group', instance.group)
        instance.password = validated_data.get('password', instance.password)
        instance.save()
        return instance


class RegisterAdminSerializer(UserSerializer):
    class Meta:
        model = Users
        fields = (
            'username', 'first_name', 'last_name',
            'email', 'password', 'confirm_passwd'
        )

    def validate(self, data):
        password = data.get('password')
        confirm = data.pop('confirm_passwd')
        if password != confirm:
            raise ValidationError('Entered passwords are not the same!')

        return data

    def create(self, validated_data):
        username = validated_data.get('username')
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        email = validated_data.get('email')
        password = validated_data.get('password')
        try:
            user = Users.objects.create(username=username, first_name=first_name,
                                        last_name=last_name, email=email, group='Admin',
                                        is_staff=True)
            user.set_password(password)
            user.save()
            return user
        except Exception as e:
            return e


class CreateBlogSerializer(ModelSerializer):
    name = CF(validators=[UniqueValidator(queryset=Blog.objects.all())], required=True, label='Name')
    description = CF(validators=[UniqueValidator(queryset=Blog.objects.all())], required=True, label='Description')
    txt = CF(validators=[UniqueValidator(queryset=Blog.objects.all())], required=True, label='Text')
    preview = IM(label='Paralax', required=True)
    img = IM(label='Image', required=False)

    def validate(self, data):
        return data

    def create(self, validated_data):
        name = validated_data.get('name')
        description = validated_data.get('description')
        txt = validated_data.get('txt')
        preview = validated_data.get('preview')
        img = validated_data.get('img')
        article = Blog.objects.create(name=name, description=description,
                                      text=txt, paralax=preview, image=img)
        article.save()
        return article


