from django.urls import path
from users.api import (
    register_user,
    users,
    user,
    list_providers,
    blacklistToken,
    search_users,
)

app_name = "users"

urlpatterns = [
    path('register/', register_user, name="register"),
    path('', users, name="users"),
    path('<int:pk>/', user, name="user"),
    path('providers',list_providers),
    path('logout/blacklist/', blacklistToken, name="blacklist"),
    path('addprovider/<str:inp>/', search_users, name="search")
]