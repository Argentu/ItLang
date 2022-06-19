from rest_framework.serializers import *
from rest_framework.serializers import CharField as CF, \
    ImageField as IF, ChoiceField as Choice,\
    ListField, DictField as DF
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

        for i in Users.objects.all():
            rel = User2Course.objects.create(course_tb=course, user_tb=i)
            rel.save()
        else:
            pass
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
    tasks = DF(required=True)

    class Meta:
        model = Lessons
        fields = 'type', 'description', \
                 'text', 'image', 'tasks'

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
        test = Tests.objects.create(lesson=lesson)
        tasks = validated_data.get('tasks')
        for i in tasks:
            task = Tasks.objects.create(type=i.get('type'), text=i.get('text'),
                                        variants='-+=+-'.join(i.get('var')),
                                        answer=i.get('ans'))
            test.tasks_for_tests.add(task)
        if validated_data.get('image'):
            for img in validated_data.pop('image'):
                img_info = Image.objects.create(image=img)
                lesson.image_material_for_lesson.add(img_info)
        lesson.save()
        return lesson

# ================Get serializers==========================


class GetCoursesSerializer(ModelSerializer):
    class Meta:
        model = Courses
        fields = 'pk', 'course_name', 'description', 'preview'


class GetLessonsSerializer(ModelSerializer):
    class Meta:
        model = Lessons
        fields = 'pk', 'descriptions',
