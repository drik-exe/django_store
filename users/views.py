from django.contrib import auth, messages
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse

from users.models import User
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('index')
    else:
        form = UserLoginForm()

    context = {
        'form': form,
    }
    return render(request, 'users/login.html', context)


def registration(request):

    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Поздравляем, вы зарегестрировались')
            username = form.cleaned_data['username']
            password = form.cleaned_data['password2']
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect('index')
    else:
        form = UserRegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'users/registration.html', context)


def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(data=request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('users:profile')
        else:
            print(form.errors)
    else:
        form = UserProfileForm(instance=request.user)
    context = {'title': 'Store - Profile', 'form': form}
    return render(request, 'users/profile.html', context)


def logout(request):
    auth.logout(request)
    return redirect('index')