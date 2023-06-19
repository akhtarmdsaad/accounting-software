from django.urls import path, include # new

urlpatterns = [
    path('', include('allauth.urls')), # new
]