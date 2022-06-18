from rest_framework.generics import *
from rest_framework.parsers import *
from rest_framework.permissions import *
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *


# Done
class CreateCourseApi(CreateAPIView):
    # permission_classes = IsAdminUser,
    QuerySet = Courses.objects.all()
    serializer_class = CreateCourseSerializer


# Done
class CreateLessonApi(CreateAPIView):
    # permission_classes = IsAdminUser,
    parser_classes = (MultiPartParser, FormParser,)
    QuerySet = Lessons.objects.all()
    serializer_class = CreateLessonSerializer

    def get_serializer_context(self):
        return {'course_id': self.kwargs.get('pk')}


# Done
class UpdateCourseApi(UpdateAPIView):
    # permission_classes = IsAdminUser,
    serializer_class = EditCourseSerializer

    def get(self, *args, **kwargs):
        lessons = []
        for i in Lessons.objects.filter(course_id=kwargs.get('pk')):
            lessons.append(i.description)
        return Response(lessons)

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'Error': 'Method PUT not allowed'})
        try:
            instance = Courses.objects.get(pk=pk)
        except:
            return Response({'Error': 'Object does not exist'})
        serializer = EditCourseSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'PUT': serializer.data, 'ID': instance.pk})


# ================Get views==========================


class GetCoursesApi(APIView):
    def get(self, *args, **kwargs):
        result = []
        for i in Courses.objects.all():
            result.append({'course_name': i.course_name,
                           'description': i.description,
                           'preview': convert_to_txt(i.preview.path)})
        return Response(result)


class GetLessonsApi(APIView):
    def get(self, *args, **kwargs):
        result = {}
        for i in Courses.objects.all():
            lessons = Lessons.objects.filter(course=i)
            img = i.preview.path
            img = convert_to_txt(img)
            result[i.pk] = {'course_name': i.course_name,
                            'description': i.description,
                            'preview': img}
            result[i.pk]['lessons'] = [i.description for i in lessons]
        return Response(result)


class GetLessonApi(APIView):
    def get(self, *args, **kwargs):
        lesson_obj = Lessons.objects.get(pk=kwargs.get('pk'))
        img = [convert_to_txt(i.image.path) for i in lesson_obj.image_material_for_lesson.filter(lesson=lesson_obj)]
        return Response({'pk': lesson_obj.pk,
                         'type': lesson_obj.type,
                         'description': lesson_obj.description,
                         'text': lesson_obj.text,
                         'images': img})

