from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .form import UserRegisterForm

# Create your views here.


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            form.save()
            messages.success(request,f'Your account has been created! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, "users/register.html", {'form':form})

@login_required
def profile(request):
    return render(request, 'users/profile.html')
