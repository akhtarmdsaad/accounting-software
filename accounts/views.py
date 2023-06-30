from django.shortcuts import render

# Create your views here.

def user_login(request):
    # Validation here 


    return render(request,"accounts/login.html")