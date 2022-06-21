from base64 import b64decode

from rest_framework.generics import *
from rest_framework.parsers import *
from django.http import JsonResponse
from rest_framework.permissions import *
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *


def get_user_id_from_token(request):
    token = request.META.get('HTTP_AUTHORIZATION', None)
    token = token.split('.')[1]
    user_json = json.loads(b64decode(token+'='))
    return user_json.get('user_id')

# Done
class CreateCourseApi(CreateAPIView):
    # permission_classes = IsAdminUser,
    QuerySet = Courses.objects.all()
    serializer_class = CreateCourseSerializer


# Done
class CreateLessonApi(CreateAPIView):
    # permission_classes = IsAdminUser,
    parser_classes = JSONParser,
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
        return Response({serializer.data})


# ================Get views==========================


class GetCoursesApi(APIView):
    def get(self, *args, **kwargs):
        result = []
        for i in Courses.objects.all():
            result.append({'course_name': i.course_name,
                           'description': i.description,
                           'preview': convert_to_txt(i.preview.path)})
        return Response({'course':result}, content_type='application/json')


class GetLessonsApi(APIView):
    def get(self, *args, **kwargs):
        result = {}
        for i in Courses.objects.all():
            lesson = Lessons.objects.filter(course=i)
            img = i.preview.path
            img = convert_to_txt(img)
            result[i.pk] = {'course_name': i.course_name,
                            'description': i.description,
                            'preview': convert_to_txt(i.preview.path)}
            tmp = [(i.description, i.pk) for i in lesson]
            dct = dict((y, x) for x, y in tmp)
            result[i.pk]['lessons'] = dct
        return Response(result)


class GetLessonApi(APIView):
    def get(self, *args, **kwargs):
        lesson_obj = Lessons.objects.get(pk=kwargs.get('pk'))
        img = [convert_to_txt(i.image.path) for i in lesson_obj.image_material_for_lesson.filter(lesson=lesson_obj)]
        return Response({'pk': lesson_obj.pk,
                         'description': lesson_obj.description,
                         'text': lesson_obj.text,
                         'images': img})


class GetTestApi(APIView):
    def get(self, *args, **kwargs):
        obj = Lessons.objects.get(pk=kwargs.get('pk')).tests
        r=[]
        for i in obj.tasks_for_tests.all():
            r.append([i.text, i.variants.split('-+=+-'), i.answer])
        res = {obj.pk: r}
        return Response(res)


class ProgressApi(UpdateAPIView):
    permission_classes = IsAuthenticated,
    serializer_class = ProgressSerializer
    QuerySet = User2Course

    def get(self, *args, **kwargs):
        user = get_user_id_from_token(self.request)
        user = Users.objects.get(pk=user)
        res={}
        for i in User2Course.objects.filter(user_tb=user):
            res[i.course_tb.course_name]=i.progress
        return Response(res)

    def put(self, request, *args, **kwargs):
        user = get_user_id_from_token(request)
        test = request.data['test']
        user = Users.objects.get(pk=user)
        course = Courses.objects.get(lessons__tests=test)
        instance = User2Course.objects.get(user_tb=user, course_tb=course)
        serializer = ProgressSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class GetCoursesForAcc(APIView):
    def get(self, *args, **kwargs):
        user = get_user_id_from_token(self.request)
        user = Users.objects.get(pk=user)
        res = {}
        for i in user.courses_set.all():
            pass
