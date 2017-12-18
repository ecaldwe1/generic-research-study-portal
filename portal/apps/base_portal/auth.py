from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate


def login_request(request):
    if request.method == 'GET':
        next = '/'
        if 'next' in request.GET:
            next = request.GET['next']

        # are they already logged in?
        if request.user.is_authenticated():
            print("HERE I AM")
            print(next)
            return redirect(next)
        else:
            return render(request, 'login.html', {'next': next})
    if request.method == 'POST':
        next = '/'
        if 'next' in request.POST:
            next = request.POST['next']

        if 'username' not in request.POST or request.POST['username'] == '':
            return render(request, 'login.html', {'error': 'missing username', 'next': next})

        if 'password' not in request.POST or request.POST['password'] == '':
            return render(request, 'login.html', {'error': 'missing password', 'next': next})

        # try to authenticate
        user = authenticate(username=request.POST['username'], password=request.POST['password'])

        # did it work?  if so, log them in and send them on their way!
        if user is not None:
            login(request, user)
            return redirect(next)
        else:
            return render(request, 'login.html', {'error': 'incorrect login', 'next': next})


def logout_request(request):
    # if they're logged in...
    if request.user.is_authenticated():
        logout(request)
        return redirect('/')
    return redirect('/')
