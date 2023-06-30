from django.urls import path, include # new
from . import views


urlpatterns = [
    path('login/',views.user_login,name = "login"),
    path('', include('allauth.urls')), # new
]