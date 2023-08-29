from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


@login_required(login_url='loginPage')
def homePage(request):
    return render(request, 'home.html')


def signupPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            return HttpResponse("Your Password is not same")
        else:
            my_user = User.objects.create_user(username, email, password1)
            my_user.save()
            return redirect("loginPage")
        # print(username, email, password1, password2)

    return render(request, 'signup.html')


def loginPage(request):
    if request.method == "POST":
        username = request.POST.get("username")
        pass1 = request.POST.get("pass")
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request, user)
            return redirect('homePage')
        else:
            return HttpResponse("username or password is incorrect")

    return render(request, 'login.html')

def logoutPage(request):
    logout(request)
    return redirect('loginPage')

