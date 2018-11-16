from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from lolina.views import set_home_page_variables
from lolina.models import Post
from .models import Profile
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from datetime import datetime
from ast import literal_eval
from urllib.parse import unquote
import time



def signup(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, f'done! you can now log in')
                return redirect('login')
        elif request.method == 'GET':
            form = UserRegisterForm()
        return render(request, 'signup.html', {'form': form})
    else:
        return redirect('homepage')


@login_required
def profile(request):
    """ user profile  """
    username = request.POST.get('username')
    if username == '0':
        user = request.user
    else:
        user = User.objects.get(username=username)

    user_posts = user.post_set.order_by('-dateNtime')[:1]
    user_posts = set_home_page_variables(user_posts)
    return JsonResponse(user_posts)


@login_required
def profile_edit_window(request):
    """ edit your profile """
    u_form = UserUpdateForm()
    p_form = ProfileUpdateForm()

    context = {
        'u_form' : u_form,
        'p_form' : p_form
    }
    return render(request, 'profile_edit_window.html', context)


#TODO: merge these 2 views!
##############################################################################
@login_required
def update_profile_info(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            context = {
                        'username': request.user.username,
                        #'email': request.user.email
                        }
            return JsonResponse(context)
        else:
            return HttpResponse('None')


@login_required
def update_profile_image(request):
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if p_form.is_valid():
            p_form.save()
            user = User.objects.get(username=request.user.username, email=request.user.email)

            context = {'profile_picture': user.profile.image.url}
            return JsonResponse(context)
        else:
            return HttpResponse('None')
###############################################################################


@login_required
def get_user_profile_picture(request):
    """ fetch profile picture of another user """
    username = request.POST.get('username')
    user = User.objects.get(username=username)

    return JsonResponse({'profile_picture': user.profile.image.url})


@login_required
def navigate_profile(request):
    home_page_vars = {}
    date = literal_eval(request.POST.get('date'))
    key  = request.POST.get('key')
    number = int(request.POST.get('number'))
    if number == 0: number = 1
    elif number > 5: number = 5


    friend = request.POST.get('username')
    if friend == 'false':
        user = request.user
    else:
        user = User.objects.get(username=friend)

    if key == 'old':
        if number != 1:
            posts = Post.objects.filter(dateNtime__lte=date, user=user).order_by('-dateNtime')[:number]
        else:
            posts = Post.objects.filter(dateNtime__lte=date, user=user).order_by('-dateNtime')[:2]
    else:   # newer markers
        if number != 1:
            posts = Post.objects.filter(dateNtime__gte=date, user=user).order_by('dateNtime')[:number]
        else:
            posts = Post.objects.filter(dateNtime__gte=date, user=user).order_by('dateNtime')[:2]

    if number == 1:
        user_posts = set_home_page_variables(posts,1)
    else:
        user_posts = set_home_page_variables(posts, number)
    return JsonResponse(user_posts)
