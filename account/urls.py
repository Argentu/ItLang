from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('reg', RegisterApi.as_view(), name='auth_register'),
    path('areg', RegisterAdminApi.as_view(), name='admin_register'),
    path('edit_user', EditUserDataApi.as_view(), name='edit'),

    path('login', MyObtainTokenPairApi.as_view(), name='token_obtain_pair'),
    path('login/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]
