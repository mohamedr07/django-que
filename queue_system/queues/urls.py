# from rest_framework import routers
# from .api import QueueViewSet

# router = routers.DefaultRouter()
# router.register('api/queues',QueueViewSet,'queues')
# urlpatterns = router.urls

from django.urls import path
from .views import queues_list,queue,join_next_queue,advance_queue,get_user_info

urlpatterns = [
    path('',queues_list),
    path('<int:pk>',queue),
    path('join',join_next_queue),
    path('<int:pk>/advance',advance_queue),
    path('<int:pk>/info',get_user_info)
]
