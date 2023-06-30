from django.shortcuts import redirect, render
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from .models import CustomUser


# Create your views here.

def user_login(request):
    # Validation here 
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        if authenticate(request,email=email,password=password):
            print("Yes authentication")
            return redirect("finance_dashboard")
        else:
            messages.error(request,"Email or Password is Incorrect")

    return render(request,"accounts/login.html")