from django.shortcuts import get_object_or_404, render, redirect

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# @login_required(login_url="/login/")
def home_view(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('myadmin')
        elif request.user.is_active:
            return redirect('home')
        # else:
            # return render(request, 'pages/not_user.html')
    return redirect('home')


def home(request):
    return render(request, 'home.html')



@login_required(login_url="/login/")
def myadmin_view(request):
    return render(request, 'pages/myadmin.html')


@login_required(login_url="/login/")
def user_list_view(request):
    # for user list and cuser count
    users = User.objects.all().filter(is_superuser='False')
    userc_active_count = User.objects.all().filter(is_active='True', is_superuser='False').count()
    users_staff_count =  User.objects.all().filter(is_staff='True', is_superuser='False').count()
    users_count = User.objects.all().filter(is_superuser='False') .count()
    u_not_active_user_count = User.objects.all().filter(is_active='False', is_superuser='False').count()
    # for pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(users, 5)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    context= {
        'users': users,
        'u_count': users_count,
        'u_a_count': userc_active_count,
        'u_s_count':users_staff_count,
        'u_not_a_user': u_not_active_user_count
    }
    return render(request, 'pages/user_list.html',context)


@login_required(login_url="/login/")
def update_view(request, id):
    user = get_object_or_404(User, id=id)
    form = UserChangeForm(request.POST or None, instance = user)
    if form.is_valid():
        form.save()
        return redirect('users')
    context = {
        'form' : form,
        'user' : user
    }
    return render(request, 'pages/user_update.html', context)


@login_required(login_url="/login/")
def delete_view(request, id):
    obj = get_object_or_404(User, id = id)
    if request.method =="POST":
        obj.delete()
        return redirect('myadmin:users')
    return render(request, "pages/delete_view.html")


@login_required(login_url="/login/")
def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            return redirect('myadmin:users')
        else:
            return render(request, 'pages/user_register.html', {'form': form})
    else:
        form = UserCreationForm()
        return render(request, 'pages/user_register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            form = AuthenticationForm(request.POST)
            return render(request, 'pages/login.html',  {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, 'pages/login.html', {'form': form})
