from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(
                    request, f"Account has been created for {form.data.get('username')}")
                return redirect('login')
        else:
            form = RegisterForm()
            context = {
                'form': form,
                'title': 'Register'
            }
            return render(request, 'user/register.html', context)

@login_required
def logout_user(request):
    logout(request)
    messages.success(request, 'You have been Logged out.')
    return redirect('home')