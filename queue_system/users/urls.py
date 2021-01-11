from django.urls import path
from users.api import (
    register_user,
    users,
    user,
    update_user,
    delete_user,
)

app_name = "users"

urlpatterns = [
    path('register/', register_user, name="register"),
    path('', users, name="users"),
    path('<str:pk>/', user, name="user"),
    path('update/<str:pk>/', update_user, name="update"),
    path('delete/<str:pk>/', delete_user, name="delete"),
]