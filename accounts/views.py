from django.shortcuts import redirect, render
from allauth.account.auth_backends import AuthenticationBackend
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from .models import CustomUser


# Create your views here.

def user_login(request):
    # Validation here 
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email,password)
        print(authenticate(request,username=email,password=password))
        if authenticate(request,email=email,password=password) or authenticate(request,username=email,password=password):
            print("Yes authentication")
            user = CustomUser.objects.get(email=email)
            login(request,user)



            # get the next parameter
            next_url = request.GET.get("next")
            if next_url:
                return redirect(next_url)
            else:
                return redirect("finance_dashboard")
        else:
            messages.error(request,"Email or Password is Incorrect")

    return render(request,"accounts/login.html")

def user_logout(request):
    logout(request)
    return redirect("login")