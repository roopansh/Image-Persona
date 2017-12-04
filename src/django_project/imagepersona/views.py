from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm

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

# User Log Out
def logout_user(request):
    logout(request)
    return HttpResponse("Logged Out Successfully!")

# Register New User
def register_user(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponse("Registered and Logged In Successfully!")
    context = { "form": form }
    return render(request, 'imagepersona/register.html', context)
