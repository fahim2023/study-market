from django.shortcuts import render

# Create your views here.
from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect, render

from .forms import RegisterForm


from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm


def register(request):
    if request.user.is_authenticated:
        # return redirect("documents:browse")
        return redirect("admin:index")  # temporary until browse view exists

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to StudyMarket, {user.username}!")
            # return redirect("documents:browse")
            return redirect("admin:index")  # temporary until browse view exists
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("admin:index")  # temporary until documents:browse exists

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect("admin:index")  # temporary until documents:browse exists
    else:
        form = AuthenticationForm()

    return render(request, "accounts/login.html", {"form": form})
