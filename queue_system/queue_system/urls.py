
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from users.views import LoginView
from django.views.generic import TemplateView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',TemplateView.as_view(template_name='index.html')),
    path('ws/', include('websocket.urls')),
    path('api/users/', include('users.urls')),
    path('api/queues/',include('queues.urls')),
    path('api/processes/',include('processes.urls')),
    path('api/stations/',include('servicestations.urls')),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
