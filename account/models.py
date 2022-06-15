from django.db.models import *
from django.contrib.auth.models import AbstractUser, PermissionsMixin


class Users(AbstractUser, PermissionsMixin):
    # main fields
    EN_LVL = [
        ('0', 'Pre-A1 Beginner'),
        ('1', 'A1 Elementary'),
        ('2', 'A2 Pre-Intermediate'),
        ('3', 'B1 Intermediate'),
        ('4', 'B2 Upper-Intermediate'),
        ('5', 'C1 Advanced'),
        ('6', 'C2 Proficiency'),
        ('7', 'Undefined')]

    first_name = CharField(max_length=15, default='blank', db_index=True)
    last_name = CharField(max_length=15, default='blank', db_index=True)
    username = CharField(max_length=15, unique=True, db_index=True)
    email = EmailField(unique=True, db_index=True)
    password = CharField(max_length=500)
    upd_time = DateTimeField(auto_now=True)
    en_lvl = CharField(choices=EN_LVL, default='7', max_length=1)
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
