from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm
from django.contrib.auth.forms import UserCreationForm


# Create your views here.

def index(request):
    return render(request, "start/index.html")


'''
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You are now logged in")
            return redirect("pit:info")
        else:
            messages.success(request, "Invalid username or password")
            return redirect("start:login")
    else:
        return render(request, "start/login.html")


def register_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            raw_password = form.cleaned_data["password1"]
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request, "You are now logged in")
            return redirect("pit:info")
    else:
        form = SignUpForm()
        return render(request, "website/register.html", {"form": form})
'''


def logout_view(request):
    logout(request)
    messages.success(request, "Logout successful")
    return redirect("start:index")
