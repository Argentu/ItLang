from edu.models import *


def upload_video(instance, filename):
    return f'videos/' \
           f'{datetime.today().date()}/' \
           f'{sha1((filename + str(datetime.now())).encode("UTF-8")).hexdigest() + "." + filename.split(".")[-1]}'


def upload_audio(instance, filename):
    return f'sounds/' \
           f'{datetime.today().date()}/' \
           f'{sha1((filename + str(datetime.now())).encode("UTF-8")).hexdigest() + "." + filename.split(".")[-1]}'


class Tasks(Model):
    TASK_TYPES = (
        ('1', 'Test with 1 answer'),
        ('2', 'Test with many answers'),
        ('3', 'Translate word/phrase'),
        )
    type = CharField(choices=TASK_TYPES, default='1', max_length=1)
    answer = CharField(max_length=500)
    variants = CharField(max_length=15)
    creation_time = DateTimeField(auto_now_add=True)
    upd_time = DateTimeField(auto_now=True)
    text = TextField(default='Lorem ipsum')
    test = ManyToManyField(Tests, related_name='tasks_for_tests')


# Materials
# --------------------------------------------------

class Audio(Model):
    sound = FileField(upload_to=upload_audio)
    creation_time = DateTimeField(auto_now_add=True)
    upd_time = DateTimeField(auto_now=True)

    lesson = ManyToManyField(Lessons, related_name='audio_material_for_lesson')
    task = ManyToManyField(Tasks, related_name='audio_material_for_tasks')


class Image(Model):
    image = ImageField(upload_to=upload_image)
    creation_time = DateTimeField(auto_now_add=True)
    upd_time = DateTimeField(auto_now=True)

    lesson = ManyToManyField(Lessons, related_name='image_material_for_lesson')
    task = ManyToManyField(Tasks, related_name='image_material_for_task')


class Video(Model):
    video = FileField(upload_to=upload_video)
    creation_time = DateTimeField(auto_now_add=True)
    upd_time = DateTimeField(auto_now=True)

    lesson = ManyToManyField(Lessons, related_name='video_material_for_lesson')
    task = ManyToManyField(Tasks, related_name='video_material_for_task')
# --------------------------------------------------
