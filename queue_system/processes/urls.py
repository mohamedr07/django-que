from django.urls import path
from .views import processes_list,process,join_process

urlpatterns = [
    path('',processes_list),
    path('<int:pk>',process),
    path('<int:pk>/join',join_process)
]
