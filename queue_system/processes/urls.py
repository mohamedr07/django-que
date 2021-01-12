from django.urls import path
from .views import processes_list,process

urlpatterns = [
    path('',processes_list),
    path('<int:pk>',process)
]
