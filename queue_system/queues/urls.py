# from rest_framework import routers
# from .api import QueueViewSet

# router = routers.DefaultRouter()
# router.register('api/queues',QueueViewSet,'queues')
# urlpatterns = router.urls

from django.urls import path
from .views import queues_list,queue

urlpatterns = [
    path('',queues_list),
    path('<int:pk>',queue)
]
