from django.urls import path
from .views import stations_list,station

urlpatterns=[
path('',stations_list),
path('<int:pk>',station)
]