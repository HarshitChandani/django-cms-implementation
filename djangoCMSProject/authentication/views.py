from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


def login_template(request):
    if request.method == "GET":
        return render(request, "login.html")


def register_template(request):
    return render(request, "register.html")


@csrf_protect
def handle_login(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            username, password = request.POST['username'], request.POST['password']
            user = authenticate(
                request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                return HttpResponse('Invalid User')
        else:
            return HttpResponse('Already Logged In')


@csrf_protect
def handle_signup(request):
    if request.method == "POST":
        first_name, last_name, username, password = request.POST['first_name'], request.POST[
            'last_name'], request.POST['username'], request.POST['password']
        if request.user.is_authenticated:
            return redirect("/")

        if not User.objects.filter(username=username).exists():

            user = User.objects.create_user(
                username=username, email=username, password=password)
            user.first_name = first_name
            user.last_name = last_name
            user.is_active = True
            user.is_superuser = False
            user.is_staff = False
            user.save()
            return redirect('authentication:loginPage')
        else:
            return HttpResponse('User already exists')


def handle_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("/")
