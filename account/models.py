from django.db.models import *
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from hashlib import sha1
from datetime import datetime


def upload_image(instance, filename):
    now = f'{datetime.today().date()}{datetime.today().time().hour}{datetime.today().time().minute}{datetime.today().time().second}'
    return f'images/' \
           f'{datetime.today().date()}/' \
           f'{sha1(filename + now.encode("UTF-8")).hexdigest() + "." + filename.split(".")[-1]}'


class Users(AbstractUser, PermissionsMixin):
    # main fields
    first_name = CharField(max_length=15, db_index=True)
    last_name = CharField(max_length=15, db_index=True)
    username = CharField(max_length=15, unique=True, db_index=True)
    email = EmailField(unique=True, db_index=True)
    password = CharField(max_length=500)
    upd_time = DateTimeField(auto_now=True)
    group = CharField(max_length=10)

    # admin fields
    is_superuser = BooleanField(default=False)
    is_staff = BooleanField(default=False)

    # technical fields
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['group']

    # Methods
    def get_full_name(self):
        return ' '.join((self.first_name, self.last_name))

    def get_short_name(self):
        return self.username


class Blog(Model):
    name = CharField(max_length=40)
    description = TextField()
    user = ForeignKey(Users, default=1, on_delete=SET_DEFAULT)
    text = TextField()
    paralax = ImageField(upload_to=upload_image)
    image = ImageField(upload_to=upload_image)
