from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from .forms import RegisterForm, LoginForm


def home(request):
    return render(request, 'authentication/home.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = CustomUser.objects.create_user(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                middle_name=form.cleaned_data['middle_name'],
                role=form.cleaned_data.get('role', 0),
                is_active=True,
            )
            login(request, user)
            return redirect('authentication:home')
    else:
        form = RegisterForm()

    return render(request, 'authentication/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('authentication:home')
            else:
                form.add_error(None, 'Invalid email or password.')
    else:
        form = LoginForm()

    return render(request, 'authentication/login.html', {'form': form})


@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    return redirect('authentication:home')


@login_required(login_url='/login/')
def user_list(request):
    if request.user.role != 1:
        return render(request, 'authentication/access_denied.html')
    users = CustomUser.objects.all()
    return render(request, 'authentication/user_list.html', {'users': users})


@login_required(login_url='/login/')
def user_detail(request, user_id):
    if request.user.role != 1:
        return render(request, 'authentication/access_denied.html')
    user = CustomUser.get_by_id(user_id)
    if user is None:
        return render(request, 'authentication/user_not_found.html')
    return render(request, 'authentication/user_detail.html', {'profile_user': user})