from django.urls import path
from .views import *

urlpatterns = [
    path('create/course', CreateCourseApi.as_view(), name='create_course'),
    path('edit/course/<int:pk>', UpdateCourseApi.as_view(), name='update_course'),

    path('create/lesson/course/<int:pk>', CreateLessonApi.as_view(), name='create_lesson'),
    #path('edit/lesson/<int:pk>', UpdateLessonApi.as_view(), name='update_lesson'),

    path('get/courses', GetCoursesApi.as_view(), name='get_courses'),
    path('get/lessons/course/<int:pk>', GetLessonsApi.as_view(), name='get_lessons'),
    path('get/lesson/<int:pk>', GetLessonApi.as_view(), name='get_lesson'),


]