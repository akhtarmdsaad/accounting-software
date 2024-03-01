from django.urls import path, include # new
from . import views


urlpatterns = [
    path('login/',views.user_login,name = "login"),
    path('logout/',views.user_logout,name = "logout"),
    path('', include('allauth.urls')), # new
]