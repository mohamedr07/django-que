from django.urls import path
from users.api import (
    register_user,
    users,
    user,
    list_providers,
    blacklistToken,
    search_users,
    set_unset_provider,
)

app_name = "users"

urlpatterns = [
    path('register/', register_user, name="register"),
    path('', users, name="users"),
    path('<int:pk>/', user, name="user"),
    path('providers',list_providers),
    path('logout/blacklist/', blacklistToken, name="blacklist"),
    path('searchusers/<str:inp>/', search_users, name="search"),
    path('setunsetprovider/<int:pk>/', set_unset_provider, name="setprovider")
]