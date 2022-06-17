from base64 import b64encode
from rest_framework.generics import *
from rest_framework.parsers import *
from rest_framework.permissions import *
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *


def convert_to_txt(file_path):
    with open(file_path, "rb") as file:
        file = b64encode(file.read()).decode('utf-8')
    return file


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
    # permission_classes = IsAdminUser
    QuerySet = Tests.objects.all()
    parser_classes = (MultiPartParser, FormParser,)
    serializer_class = CreateTestSerializer

    def get_serializer_context(self):
        return {'lesson_id': self.kwargs.get('pk')}



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


# class UpdateLessonApi(UpdateAPIView):
#     # permission_classes = IsAdminUser
#     serializer_class = EditLessonSerializer
#     def put(self, request, *args, **kwargs):
#         pk = kwargs.get('pk', None)
#         if not pk:
#             return Response({'Error': 'Method PUT not allowed'})
#         try:
#             instance = Lessons.objects.get(pk=pk)
#         except:
#             return Response({'Error': 'Object does not exist'})
#         serializer = EditLessonSerializer(data=request.data, instance=instance)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({'PUT': serializer.data, 'ID': instance.pk})


class UpdateTestApi(UpdateAPIView):
    permission_classes = IsAdminUser,


# ================Get views==========================


class GetCoursesApi(ListAPIView):
    permission_classes = AllowAny,
    queryset = Courses.objects.all()
    serializer_class = GetCoursesSerializer


class CustomRenderer(renderers.BaseRenderer):
    media_type = 'image/png'
    format = 'png'
    charset = None
    render_style = 'binary'

    def render(self, data, media_type=None, renderer_context=None):
        return data


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
        # audio = lesson_obj.audio_material_for_lesson.all()
        # video = lesson_obj.video_material_for_lesson.all()
        return Response({'pk': lesson_obj.pk,
                         'type': lesson_obj.type,
                         'description': lesson_obj.description,
                         'text': lesson_obj.text,
                         'images': img})
