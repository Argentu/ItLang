from django.db.models import *
from account.models import *
from django.core.validators import MinValueValidator, MaxValueValidator


class Courses(Model):
    course_name = CharField(max_length=25, unique=True)
    description = TextField(unique=True)
    preview = ImageField(upload_to=upload_image)
    creation_time = DateTimeField(auto_now_add=True)
    upd_time = DateTimeField(auto_now=True)

    users = ManyToManyField(Users, through='User2Course')


class Lessons(Model):
    LESSON_TYPES = [
        ('1', 'Text'),
        ('2', 'Audio'),
        ('3', 'Video'),
        ('4', 'Image')
    ]
    description = CharField(max_length=40)
    type = CharField(choices=LESSON_TYPES, default='1', max_length=1)
    course = ForeignKey(Courses, on_delete=CASCADE, default=1)
    creation_time = DateTimeField(auto_now_add=True)
    upd_time = DateTimeField(auto_now=True)
    text = TextField(default='Lorem ipsum')


class Tests(Model):
    creation_time = DateTimeField(auto_now_add=True)
    upd_time = DateTimeField(auto_now=True)
    lesson = OneToOneField(Lessons, on_delete=CASCADE)


# ==================================================

# CONNECTING TABLES
# ==================================================
class User2Course(Model):
    user_tb = ForeignKey(Users, on_delete=CASCADE)
    course_tb = ForeignKey(Courses, on_delete=CASCADE)
    progress = FloatField(default=0,
                          validators=[MinValueValidator(0),
                                      MaxValueValidator(100)])
    is_finished = BooleanField(default=False)
    min_percent = PositiveSmallIntegerField(default=80,
                                            validators=
                                            [MinValueValidator(50),
                                             MaxValueValidator(100)])
