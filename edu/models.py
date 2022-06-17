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

    result = ManyToManyField(Users, through='Result')


class Tests(Model):
    TEST_TYPES = [
        ('1', 'English level'),
        ('2', 'Exam for course')
    ]
    type = CharField(choices=TEST_TYPES, max_length=1)
    description = TextField(max_length=70)
    preview = ImageField(upload_to=upload_image, blank=True)
    creation_time = DateTimeField(auto_now_add=True)
    upd_time = DateTimeField(auto_now=True)

    courses = ManyToManyField(Courses, related_name='test_for_course')
    en_lvl = ManyToManyField(Users, through='En_lvl_results')


# ==================================================

# CONNECTING TABLES
# ==================================================
class User2Course(Model):
    user_tb = ForeignKey(Users, on_delete=CASCADE)
    course_tb = ForeignKey(Courses, on_delete=CASCADE)
    progress = PositiveSmallIntegerField(default=0,
                                         validators=[MinValueValidator(0),
                                                     MaxValueValidator(100)])
    is_finished = BooleanField(default=False)
    min_percent = PositiveSmallIntegerField(default=100,
                                            validators=
                                            [MinValueValidator(50),
                                             MaxValueValidator(100)])


class Result(Model):
    user = ForeignKey(Users, on_delete=CASCADE)
    lesson = ForeignKey(Lessons, on_delete=CASCADE, related_name='intermediate_tb_for_lessons_results')
    is_finished = BooleanField(default=False)
    creation_time = DateTimeField(auto_now_add=True)
    upd_time = DateTimeField(auto_now=True)


class En_lvl_results(Model):
    user_tb = ForeignKey(Users, on_delete=CASCADE)
    test_tb = ForeignKey(Tests, on_delete=CASCADE)
    result = PositiveSmallIntegerField(validators=[MinValueValidator(0),
                                                   MaxValueValidator(120)])
    creation_time = DateTimeField(auto_now_add=True)
    upd_time = DateTimeField(auto_now=True)