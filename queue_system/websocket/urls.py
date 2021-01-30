from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:queue_id>/', views.queue, name='queue'),
]