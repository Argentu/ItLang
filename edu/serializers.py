from rest_framework.serializers import *
from rest_framework.serializers import CharField as CF, \
    ImageField as IF, ChoiceField as Choice,\
    ListField, DictField as DF
from rest_framework.validators import UniqueValidator
from base64 import b64encode
from materials.models import *


def convert_to_txt(file_path):
    with open(file_path, "rb") as file:
        file = b64encode(file.read()).decode('utf-8')
    return file


# Done
class CreateCourseSerializer(ModelSerializer):
    course_name = CF(max_length=25,
                     validators=[UniqueValidator(queryset=Courses.objects.all())],
                     label='Course name')
    description = CF(label='Description', validators=[UniqueValidator(queryset=Courses.objects.all())])
    preview = IF(label='Preview')

    class Meta:
        model = Courses
        fields = 'course_name', 'description', 'preview'

    def validate(self, data):
        if data.get('course_name') and data.get('description'):
            return data
        else:
            return ValidationError('Name and description should not be blank')

    def create(self, validated_data):
        course_name = validated_data.get('course_name')
        description = validated_data.get('description')
        preview = validated_data.get('preview')
        course = Courses.objects.create(course_name=course_name, description=description, preview=preview)
        course.save()
        return course


# Done
class EditCourseSerializer(CreateCourseSerializer):
    course_name = CF(label='Course_name', required=False)
    description = CF(label='Description', required=False)
    preview = IF(label='Preview', required=False)

    def validate(self, data, *args, **kwargs):
        return data

    def update(self, instance, validated_data):
        instance.course_name = validated_data.get('course_name', instance.course_name)
        instance.description = validated_data.get('description', instance.description)
        instance.preview = validated_data.get('preview', instance.preview)
        instance.save()
        return instance


class CreateLessonSerializer(ModelSerializer):
    LESSON_TYPES = [
        ('1', 'Text'),
        ('2', 'Audio'),
        ('3', 'Video'),
        ('4', 'Image')
    ]
    type = Choice(choices=LESSON_TYPES, default=1, label='Chose lesson type')
    description = CF(max_length=40, required=True,
                     label='Meta info for lesson (e.g. "1.3 Present simple")', )
    text = CF(validators=[UniqueValidator(queryset=Lessons.objects.all())], required=True)
    image = ListField(label='Image files', required=False, child=IF())

    # audio = ListField(label='Audio files', required=False, child=FF())
    # video = ListField(label='Video files', required=False, child=FF())

    class Meta:
        model = Lessons
        fields = 'type', 'description', \
                 'text', 'image', 'audio', 'video'

    def validate(self, data):
        if data.get('description'):
            return data
        else:
            return ValidationError('Description should not be blank')

    def create(self, validated_data):
        type = validated_data.get('type')
        description = validated_data.get('description')
        course_id = Courses.objects.get(pk=self.context['course_id'])
        text = validated_data.get('text')

        lesson = Lessons.objects.create(description=description, type=type,
                                        course=course_id, text=text)

        if validated_data.get('image'):
            for img in validated_data.pop('image'):
                img_info = Image.objects.create(image=img)
                lesson.image_material_for_lesson.add(img_info)
        # if validated_data.get('audio'):
        #     for aud in validated_data.pop('audio'):
        #         audio_info = Audio.objects.create(sound=aud)
        #         lesson.audio_material_for_lesson.add(audio_info)
        # if validated_data.get('video'):
        #     for vid in validated_data.pop('video'):
        #         video_info = Video.objects.create(video=vid)
        #         lesson.video_material_for_lesson.add(video_info)
        lesson.save()
        return lesson


# TOD
# class EditLessonSerializer(ModelSerializer):
#     LESSON_TYPES = [
#         ('1', 'Text'),
#         ('2', 'Audio'),
#         ('3', 'Video'),
#         ('4', 'Image')
#     ]
#     type = Choice(choices=LESSON_TYPES, default=1, label='Chose lesson type')
#     description = CF(max_length=40, required=True,
#                      label='Meta info for lesson (e.g. "1.3 Present simple")', )
#     text = CF(validators=[UniqueValidator(queryset=Lessons.objects.all())], required=True)
#     image = ListField(label='Image files', required=False, child=IF())
#
#     def validate(self, data):
#         return data
#
#     def update(self, instance, validated_data):
#         instance.type = validated_data.get('type', instance.type)
#         instance.description = validated_data.get('description', instance.description)
#         instance.text = validated_data.get('text', instance.text)
#         instance.type = validated_data.get('type', instance.type)
#
#         type = validated_data.get('type')
#         description = validated_data.get('description')
#         course_id = Courses.objects.get(pk=self.context['course_id'])
#         text = validated_data.get('text')
#         lesson = Lessons.objects.create(description=description, type=type,
#                                                  course=course_id, text=text)
#         if validated_data.get('image'):
#             if len(validated_data.get('image'))==len(instance.image_material_for_lesson.all()):
#                 for i, k in zip(instance.image_material_for_lesson.all(), validated_data.get('image')):
#                     i.image = k
#             elif len(validated_data.get('image'))>len(instance.image_material_for_lesson.all()):
#                 counter = 0
#                 for i in validated_data.get('image'):
#                     if
#
#             for img in validated_data.pop('image'):
#                 img_info = Image.objects.create(image=img)
#                 lesson.image_material_for_lesson.add(img_info)
#         lesson.save()
#         return lesson


class CreateTestSerializer(ModelSerializer):
    description = CF(label='Description')
    tasks: DF()

    class Meta:
        model = Tests
        fields = 'description', 'tasks'

    def validate(self, data):
        if data.get('description'):
            return data
        else:
            return ValidationError('Description should not be blank')

    def create(self, validated_data):
        description = validated_data.get('description')
        lesson_id = self.context['lesson_id']
        test = Tests.objects.create(description=description, lesson_id=lesson_id)
        for i in validated_data.get('tasks'):
            task = Tasks.objects.create(type=i.get('type'), text=i.get('text'),
                                        variants='-+=+-'.join(i.get('var')),
                                        answer=i.get('ans'))
        test.tasks_for_tests.add(task)
        test.save()
        return test



# ================Get serializers==========================


class GetCoursesSerializer(ModelSerializer):
    class Meta:
        model = Courses
        fields = 'pk', 'course_name', 'description', 'preview'


class GetLessonsSerializer(ModelSerializer):
    class Meta:
        model = Lessons
        fields = 'pk', 'descriptions',
