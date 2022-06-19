from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('reg', RegisterApi.as_view(), name='auth_register'),
    path('areg', RegisterAdminApi.as_view(), name='admin_register'),
    path('edit_user', EditUserDataApi.as_view(), name='edit'),

    path('login', MyObtainTokenPairApi.as_view(), name='token_obtain_pair'),
    path('login/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('create/blog', CreateBlogApi.as_view(), name='create_blog'),
    path('get/blogs', GetBlogsApi.as_view(), name='get_blogs'),
    path('get/blog/<int:pk>', GetBlogApi.as_view(), name='get_blog'),
    path('update/blog/<int:pk>', UpdateBlogApi.as_view(), name='update_blog')
]
