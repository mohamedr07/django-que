from django.urls import path
from users.api import (
    register_user,
    users,
    user,
)

app_name = "users"

urlpatterns = [
    path('register/', register_user, name="register"),
    path('', users, name="users"),
    path('<int:pk>/', user, name="user"),
]