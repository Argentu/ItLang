from rest_framework.serializers import *
from rest_framework.serializers import CharField as CF, \
    ImageField as IF, IntegerField as INT,\
    ListField, DictField as DF
from rest_framework.validators import UniqueValidator
from materials.models import *


def toFixed(numObj):
    return f"{numObj:.{2}f}"

# Done
class CreateCourseSerializer(ModelSerializer):
    class hide__:
        def __init__(self, name, des, pr, minp):
            self.course_name = name
            self.description = des
            self.preview = pr
            self.min_percent = minp

    course_name = CF(max_length=25,
                     validators=[UniqueValidator(queryset=Courses.objects.all())],
                     label='Course name')
    description = CF(label='Description', validators=[UniqueValidator(queryset=Courses.objects.all())])
    preview = IF(label='Preview')
    min_percent = INT()

    class Meta:
        model = Courses
        fields = 'course_name', 'description', 'preview', 'min_percent'

    def validate(self, data):
        if data.get('course_name') and data.get('description'):
            return data
        else:
            return ValidationError('Name and description should not be blank')

    def create(self, validated_data):
        course_name = validated_data.get('course_name')
        description = validated_data.get('description')
        preview = validated_data.get('preview')
        per = validated_data.get('min_percent', None)
        course = Courses.objects.create(course_name=course_name, description=description, preview=preview)
        if per:
            for i in Users.objects.all():
                rel = User2Course.objects.create(course_tb=course, user_tb=i, min_percent=per)
                rel.save()
        else:
            for i in Users.objects.all():
                rel = User2Course.objects.create(course_tb=course, user_tb=i)
                rel.save()
        course.save()
        c = self.hide__(name=course.course_name, des=course.description, pr=course.preview, minp=course.user2course_set.all()[0].min_percent)
        return c


# Done
class EditCourseSerializer(CreateCourseSerializer):
    course_name = CF(label='Course_name', required=False)
    description = CF(label='Description', required=False)
    preview = IF(label='Preview', required=False)
    min_percent = INT()

    def validate(self, data, *args, **kwargs):
        return data

    def update(self, instance, validated_data):
        instance.course_name = validated_data.get('course_name', instance.course_name)
        instance.description = validated_data.get('description', instance.description)
        instance.preview = validated_data.get('preview', instance.preview)
        per = validated_data.get('min_percent', instance.user2course_set.all()[0].min_percent)
        for i in instance.user2course_set.all():
            i.min_percent = per
            i.save()
        instance.save()
        return instance


class hide:
    def __init__(self, description, text, image, tasks):
        self.description=description
        self.text=text
        self.image=image
        self.tasks=tasks

class CreateLessonSerializer(Serializer):
    description = CF(max_length=40, required=True,
                     label='Meta info for lesson (e.g. "1.3 Present simple")', )
    text = CF(validators=[UniqueValidator(queryset=Lessons.objects.all())], required=True)
    image = ListField(label='Image files', required=False, child=IF())
    tasks = DF(required=True)

    def validate(self, data):
        if data.get('description'):
            return data
        else:
            return ValidationError('Description should not be blank')

    def create(self, validated_data):
        description = validated_data.get('description')
        course_id = Courses.objects.get(pk=self.context['course_id'])
        text = validated_data.get('text')
        lesson = Lessons.objects.create(description=description,
                                        course=course_id, text=text)
        test = Tests.objects.create(lesson=lesson)
        tasks = validated_data.get('tasks')['tasks']
        for i in tasks:
            task = Tasks.objects.create(text=i.get('text'),
                                        variants='-+=+-'.join(i.get('var')),
                                        answer=i.get('ans'),
                                        test=test)
            task.save()
        if validated_data.get('image'):
            for img in validated_data.pop('image'):
                img_info = Image.objects.create(image=img)
                lesson.image_material_for_lesson.add(img_info)
        lesson.save()
        less = hide(description=lesson.description, text=lesson.text,
                    image={"images":[convert_to_txt(i.image.path) for i in lesson.image_material_for_lesson.all()]},
                    tasks={"tasks":[i.text for i in lesson.tests.tasks_for_tests.all()]})
        return less


class hide_:
    def __init__(self, test, res):
        self.test = test
        self.res = res

class ProgressSerializer(ModelSerializer):
    test = CF()
    res = INT()

    class Meta:
        model = User2Course
        fields = 'test', 'res'

    def update(self, instance, validated_data):
        lessons = len(instance.course_tb.lessons_set.all())
        res = validated_data.get('res')
        per = 100/lessons/10
        instance.progress += float(toFixed(res*per))
        if instance.progress >= instance.min_percent:
            instance.is_finished = True
        instance.save()
        less = hide_(test=validated_data.get('test'), res=instance.progress)
        return less



# ================Get serializers==========================


class GetCoursesSerializer(ModelSerializer):
    class Meta:
        model = Courses
        fields = 'pk', 'course_name', 'description', 'preview'


class GetLessonsSerializer(ModelSerializer):
    class Meta:
        model = Lessons
        fields = 'pk', 'descriptions',
