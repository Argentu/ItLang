from django.urls import path, include

urlpatterns = (
    path('acc/', include('account.urls')),
    path('edu/', include('edu.urls')),
)
