from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


def index(request):
	return HttpResponse("Main Index Page")

# user log in
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponse("Login Successful!")
            else:
                return render(request, 'imagepersona/login.html', {'login_error_message': 'Your account has been disabled'})
        else:
            return render(request, 'imagepersona/login.html', {'login_error_message': 'Invalid login'})
    return render(request, 'imagepersona/login.html')

# User Log Out
def logout_user(request):
    logout(request)
    return render(request, 'imagepersona/login.html')

# Register New User
def register_user(request):
    if request.method == "POST":
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.create_user(username, email, password)
        user.last_name = lastname
        user.first_name = firstname
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponse("Registered and Logged In Successfully!")
    return render(request, 'imagepersona/login.html')
