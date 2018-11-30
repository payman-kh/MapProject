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


"""
 the sign up form
 this function first checks whether the user is already logged in. if logged in,
 it redirects to the homepage,
 if not it checks whether the request is POST or GET. if the request is GET,
 it means the page has just been opened an or refreshed, and the sing up form
 appears and the user can sign up.
 if the request is post, it means a new user has already filled in the form and
 submitted it. so a new user is created and is redirected to the log in page,
 where he can log in.
"""
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


"""
this function is called when the user clicks on the profile button (the small
image) on the navbar or goes to another user's profile.
this function checks wether the user is going to his profile or someone elses's
profile.
it then queries the last markers of that profile and sends back as a JsonResponse
"""
@login_required
def profile(request):
    """ user profile  """

    # if user is going to his own profile, this variable is zero
    username = request.POST.get('username')

    #own profile or someone else's profile?
    if username == '0':
        user = request.user
    else:
        user = User.objects.get(username=username)

    user_posts = user.post_set.order_by('-dateNtime')[:1]
    user_posts = set_home_page_variables(user_posts, request.user)
    return JsonResponse(user_posts)


"""
the form for updating the profile
when the user is on her own profile, the small edit button is on the profile
window. once it is clicked a modal window (defined in the fron-end) pops up.
then this function is called. it fetches UserUpdateForm and ProfileUpdateForm
defined in forms.py and renders them on that modal window. so the user can update
her profile.
the forms are displayed using crispy_formss
"""
@login_required
def profile_edit_window(request):
    """ edit your profile """
    # update username and email
    u_form = UserUpdateForm()
    #update profile picture
    p_form = ProfileUpdateForm()

    context = {
        'u_form' : u_form,
        'p_form' : p_form
    }
    return render(request, 'profile_edit_window.html', context)


"""
updating the profile information (at the moment only username, email and profile
picture)
similar to saving a new marker, this is a two step procedure. once the user submits
new entries on the from created with the function above:

1. an ajax call comes to "update_profile_info" containing the new name and the new
email. it checkes if the entries are valid and saves them. it then send the new
username back to the ajax's success function which is then used to update the name
on the profile window (yes, this could be done completely on the client side)

2. in the success function, there is another ajax call (it is a nested ajax),
which takes the new image and comes to the second function "update_profile_image".
it checkes if it is valid and updates the image on the database. then sends back
the image to the second ajax's success where it is used to update the profile
image on the profile window (this could also completely be done on the clint side
not on the ajax's success)
"""
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


"""
when the user visits someone's profile, this function is called. it gets the
profile pictue of this profile and sends back to to front-end so it can be put
on the profile window
"""
@login_required
def get_user_profile_picture(request):
    """ fetch profile picture of another user """
    username = request.POST.get('username')
    user = User.objects.get(username=username)
    return JsonResponse({'profile_picture': user.profile.image.url})


"""
when the user is on a profile (own's profile or someone else's profile), and
starts navigating through the markers in that profile, this function is called
in each navigation attempt by ajax.
it is almost the same as "homepage" function. but here only markers of one
particular user is queried on each navigation.
it always checks whether the user is on his own profile or someone else's profile.
"""
@login_required
def navigate_profile(request):
    """
    navigate through a profiles markers
    """
    home_page_vars = {}
    date = literal_eval(request.POST.get('date'))
    key  = request.POST.get('key')
    number = int(request.POST.get('number'))
    if number == 0: number = 1
    elif number > 5: number = 5

    # is the user on his own profile, or someone else's profile?
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
        user_posts = set_home_page_variables(posts, request.user, 1)
    else:
        user_posts = set_home_page_variables(posts, request.user, number)
    return JsonResponse(user_posts)


"""
once the user clicks on "delete account" on the navbar, this function deletes
the user (and so the associated profile) from the database and the user is
redirected to the sign up page.
"""
@login_required
def deleteAccount(request):
    user = request.user
    user = User.objects.filter(username=user.username, email=user.email)
    user.delete()
    return redirect('logout')
