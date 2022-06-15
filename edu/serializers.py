from rest_framework.serializers import *
from rest_framework.serializers import CharField as CF, \
    ImageField as IF, ChoiceField as Choice, \
    FileField as FF, ListField
from rest_framework.validators import UniqueValidator

from materials.models import *


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
    description = CF(label='Description', required=False)
    preview = IF(label='Preview', required=False)

    def validate(self, data, *args, **kwargs):
        if data.get('course_name'):
            return data
        else:
            return ValidationError('Name should not be blank')

    def update(self, instance, validated_data):
        instance.course_name = validated_data.get('course_name', instance.course_name)
        instance.description = validated_data.get('description', instance.description)
        instance.preview = validated_data.get('preview', instance.preview)
        instance.save()
        return instance


# Done
class CreateThemeSerializer(ModelSerializer):
    theme_name = CF(max_length=25,
                    label='Theme name')
    description = CF(label='Description')
    preview = IF(label='Preview')

    class Meta:
        model = Themes
        fields = 'theme_name', 'description', 'preview'

    def validate(self, data):
        if data.get('theme_name') and data.get('description'):
            return data
        else:
            return ValidationError('Name and description should not be blank')

    def create(self, validated_data):
        theme_name = validated_data.get('theme_name')
        description = validated_data.get('description')
        preview = validated_data.get('preview')
        course_id = self.context['course_id']
        theme = Themes.objects.create(theme_name=theme_name, description=description, preview=preview,
                                      course_id=course_id)
        theme.save()
        return theme


# Done
class EditThemeSerializer(CreateThemeSerializer):
    description = CF(label='Description', required=False)
    preview = IF(label='Preview', required=False)

    def validate(self, data, *args, **kwargs):
        if data.get('theme_name'):
            return data
        else:
            return ValidationError('Name should not be blank')

    def update(self, instance, validated_data):
        instance.theme_name = validated_data.get('theme_name', instance.theme_name)
        instance.description = validated_data.get('description', instance.description)
        instance.preview = validated_data.get('preview', instance.preview)
        instance.save()
        return instance


class hide:
    def __init__(self, type, description, text):
        self.type = type
        self.description = description
        self.text = text


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
    text = CF(validators=[UniqueValidator(queryset=Text.objects.all())])
    image = ListField(label='Image files', required=False, child=IF())
    audio = ListField(label='Audio files', required=False, child=FF())
    video = ListField(label='Video files', required=False, child=FF())

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
        theme_id = self.context['theme_id']

        lesson: Lessons = Lessons.objects.create(description=description, type=type,
                                                 theme_id=theme_id)

        text = validated_data.get('text')
        text_info = Text.objects.create(text=text)
        lesson.text_material_for_lesson.add(text_info)
        less = hide(type=type, description=description, text=text)

        if validated_data.get('image'):
            for img in validated_data.pop('image'):
                img_info = Image.objects.create(image=img)
                lesson.image_material_for_lesson.add(img_info)
        if validated_data.get('audio'):
            for aud in validated_data.pop('audio'):
                audio_info = Audio.objects.create(sound=aud)
                lesson.audio_material_for_lesson.add(audio_info)
        if validated_data.get('video'):
            for vid in validated_data.pop('video'):
                video_info = Video.objects.create(video=vid)
                lesson.video_material_for_lesson.add(video_info)
        lesson.save()
        return less


class CreateTestSerializer(ModelSerializer):
    description = CF(label='Description')
    preview = IF(label='Preview')

    class Meta:
        model = Themes
        fields = 'description', 'preview'

    def validate(self, data):
        if data.get('description'):
            return data
        else:
            return ValidationError('Description should not be blank')

    def create(self, validated_data):
        description = validated_data.get('description')
        preview = validated_data.get('preview')
        course_id = self.context['course_id']
        test = Tests.objects.create(description=description, preview=preview,
                                    course_id=course_id)
        test.save()
        return test

# ================Get serializers==========================

class GetCoursesSerializer(ModelSerializer):
    class Meta:
        model = Courses
        fields = 'pk', 'course_name', 'description', 'preview'


class GetThemesSerializer(ModelSerializer):
    class Meta:
        model = Themes
        fields = 'theme_name', 'description', 'preview'


class GetLessonsSerializer(ModelSerializer):
    class Meta:
        model = Lessons
        fields = 'pk', 'description'
