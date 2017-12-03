from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout


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
                return render(request, 'imagepersona/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'imagepersona/login.html', {'error_message': 'Invalid login'})
    return render(request, 'imagepersona/login.html')

