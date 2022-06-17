from rest_framework import viewsets
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


class CreateTestApi(CreateAPIView):
    permission_classes = IsAdminUser


# Done
class UpdateCourseApi(UpdateAPIView):
    # permission_classes = IsAdminUser,
    serializer_class = EditCourseSerializer

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


class UpdateLessonApi(CreateLessonApi):
    pass


class UpdateTestApi(UpdateAPIView):
    permission_classes = IsAdminUser,


# ================Get views==========================


class GetCoursesApi(ListAPIView):
    permission_classes = AllowAny,
    queryset = Courses.objects.all()
    serializer_class = GetCoursesSerializer


class GetLessonsApi(ListAPIView):
    permission_classes = AllowAny,
    serializer_class = GetLessonsSerializer

    def get_queryset(self):
        course = self.kwargs.get('pk')
        return Lessons.objects.filter(course_id=course)


class GetLessonApi(APIView):

    def get(self, *args, **kwargs):
        lesson_obj = Lessons.objects.get(pk=kwargs.get('pk'))
        img = [i.get('image') for i in lesson_obj.image_material_for_lesson.filter(lesson=lesson_obj).values()]
        audio = lesson_obj.audio_material_for_lesson.all()
        video = lesson_obj.video_material_for_lesson.all()
        return Response({'pk': lesson_obj.pk,
                         'type': lesson_obj.type,
                         'description': lesson_obj.description,
                         'text': lesson_obj.text,
                         'images': img,
                         'audios': audio,
                         'videos': video})
