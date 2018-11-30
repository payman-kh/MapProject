from django.shortcuts import render , redirect
from django.http import JsonResponse, HttpResponse
from .models import Post , Comment, Like #, SearchQueries
#from users.models import Profile
from django.contrib.auth.models import User
import json
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime
#import requests
from ast import literal_eval
from urllib.parse import unquote
from django.contrib.auth.decorators import login_required
from django.db.models import Q
#import os




"""
this function receives a query of markers from another function and makes a json
of all the varibales which are needed for displaying the queried markers in frot-end.

The variables include:
1. markers_json: the attributes of the queried markers (title, body, image, video,
link)

2. user_name: name of the users that added the markers in markers_jason. they
are listed with the same order as markers_jason

3. image_urls: profile image of these users with the same order (to be shown) next
to the marker's title

4. ids: unique IDs of the markers with the same order

5. num_likes: number of likes of the posts listed with the same order

6. liked: a list of boolean which denotes whether the current user querying, has
liked these markers or not. has the same order

7. min_datetime: the oldest "upload date" of the posts. in other words tells when
the oldes one (of the queried markers) was posted

8. max_datetime: the newest markers upload date

9. number: the number of queried markers
"""
def set_home_page_variables(posts, user, number=1):
    home_page_dict = {}
    if posts:
        json_serializer = serializers.get_serializer("json")()
        markers_json = json_serializer.serialize(posts  , ensure_ascii=False)

        user_names  = [ p.user.username for p in posts ]
        user_names_json =  json.dumps(user_names, cls=DjangoJSONEncoder)

        image_urls  = [ p.user.profile.image.url for p in posts ]
        image_urls_json =  json.dumps(image_urls, cls=DjangoJSONEncoder)

        ids = [ p.pk for p in posts ]
        ids_json =  json.dumps(ids, cls=DjangoJSONEncoder)

        num_likes = [Like.objects.filter(post=p).count() for p in posts]
        num_likes_json = json.dumps(num_likes, cls=DjangoJSONEncoder)

        liked = [0] * posts.count()
        user_id = int(user.id)
        for i, p in enumerate(posts):
            likes = Like.objects.filter(post=p).values()
            for l in likes:
                if user_id == l['user_id']: liked[i] = 1
        liked_json = json.dumps(liked, cls=DjangoJSONEncoder)

        posts_list = posts.values()
        datetimes  = [ d['dateNtime'] for d in posts_list ]
        min_datetime = str(min(datetimes))
        max_datetime = str(max(datetimes))
        min_datetime_json = json.dumps(min_datetime, cls=DjangoJSONEncoder)
        max_datetime_json = json.dumps(max_datetime, cls=DjangoJSONEncoder)

        home_page_dict = {'markers_json': markers_json,
                          'user_names'  : user_names_json,
                          'image_urls'  : image_urls_json,
                          'ids'         : ids_json,
                          'num_likes'   : num_likes_json,
                          'liked'       : liked_json,
                          'min_datetime': min_datetime_json,
                          'max_datetime': max_datetime_json,
                          'number'      : number}
    return home_page_dict




"""
this function queries the last marker(s) by friends to be shown on the home page
anytime the user clicks on the "home" button on the navbar. then sends it to
"set_home_page_variables()" function to get the json with all the varibales for
this (or these) marker(s). then send a JsonResponse containing this json file to
the front-end
"""
def get_latest_markers(requests):
    """latest markers added by friends (anyone but you)"""
    user = requests.user
    posts = Post.objects.exclude(user=user).filter(dateNtime__lte=datetime.now()).order_by('-dateNtime')[:1]
    home_page_vars = set_home_page_variables(posts, user)
    return JsonResponse(home_page_vars)


"""
this function first checks whether the user is logged in. if not redirects to the
log out page.

if logged in, it checks whether the request is ajax or not:

1.if it is not ajax, it means that it is the first time the page is called (the user
has just opened or refreshed the website). so like the previous function, it fetches
the last marker(s), makes the json and renders the map showing the last marker(s).

2.if request is ajax, it means the user is already on the map (homepage) but wants
to navigate through markers, either going to older ones or newer ones. so the
function first checkes whether it is a request for older ones or newer ones and
then queries the database for markers with older or newer dates. makes the json
and sends back a JsonResponse.
"""
@login_required
def homepage(requests):
    user = requests.user
    if "logged-in":
        home_page_vars = {}
        if requests.method == "POST" and requests.is_ajax():

            number = int(requests.POST.get('number'))
            if number <= 0: number = 1
            elif number > 5: number = 5
            date = literal_eval(requests.POST.get('date'))
            key  = requests.POST.get('key')

            if key == 'old':   # older markers
                if number != 1:
                    posts = Post.objects.exclude(user=user).filter(dateNtime__lte=date).order_by('-dateNtime')[:number]
                else:
                    posts = Post.objects.exclude(user=user).filter(dateNtime__lte=date).order_by('-dateNtime')[:2]
            else:   # newer markers
                if number != 1:
                    posts = Post.objects.exclude(user=user).filter(dateNtime__gte=date).order_by('dateNtime')[:number]
                else:
                    posts = Post.objects.exclude(user=user).filter(dateNtime__gte=date).order_by('dateNtime')[:2]

            #if number == 1:
            #    home_page_vars = set_home_page_variables(posts)
            #else:
            home_page_vars = set_home_page_variables(posts, user, number)
            return JsonResponse(home_page_vars)

        else:       # first time homepage load
            posts = Post.objects.exclude(user=user).order_by('-dateNtime')[:2]
            home_page_vars = set_home_page_variables(posts, user, 1)
            return render(requests, 'map.html', home_page_vars)
    else:
        return redirect('login')



"""
searching for other users using the search bar on the navbar.
it looks in the database for user(s) with the same name as the word entered by
the user. it is actually not a search function. just a form. it does not search
for similar entries nor does it suggest anything. once it finds a result,
sends back a JsonResponse containing these usernames

at the moment the search bar is only for searching for other users. not for
searcing for markers!
"""
def Search(request):
    """ search for a user """
    q = request.GET.get('q')
    #users = User.objects.filter(Q(username__icontains=requests.POST.get('q'))
    #| Q(name__icontains=requests.POST.get('q')))
    users = User.objects.filter(Q(username__icontains=request.GET.get('q'))).values('username')
    if users:
        return JsonResponse({'users': list(users)})
    else:
        return JsonResponse({'users': None})


"""
these two successive functions save a new marker in the data base. the new markers
can have data (title, body, youtube url) and files (images and videos)

1.first SaveMarker1, receives an ajax request containing the new marker's data:
title (which is required), body and youtube url. and saves the marker with this
attributes in the database. so the new marker is saved at this point. then it
checks the attribute "file_data" of this marker. if it is false, this means there
are no files added on the marker, so saving the marker is done. however ...

2. if file_data is true, this means there are images or videos to be saved on the
marker. so the request goes into the "success function" of this ajax. inside this
function there is another ajax (this is a nested ajax). here the "files" are sent
to SaveMarker2. this function queries the last marker added by the user and adds
the files to it.

the problem was that i could not find an easy way to send data and files together
so I made this a two step process
"""
###############################################################################
def SaveMarker1(request):
    """ save a new marker to the database and send it back"""
    """ not saving the image/video """
    if request.method == 'POST':
        user = request.user
        title = unquote(request.POST.get('title'))
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        was_there = unquote(request.POST.get('was_there'))
        if was_there == 'true': was_there = True
        else: was_there = False

        just_saved_marker = Post.objects.create(title=title,
                                                latitude=latitude,
                                                longitude=longitude,
                                                user=user,
                                                was_there=was_there)

        try:
            body = unquote(request.POST.get('body'))
            just_saved_marker.body = body
            just_saved_marker.save()
        except:
            pass
        try:
            youtube_url = request.POST.get('youtube_url')
            just_saved_marker.youtube_url = youtube_url
            just_saved_marker.save()
        except:
            pass

    if request.POST.get('file_data') == 'false':
        # user is redirected to the profile after adding a post (marker)
        user_posts = Post.objects.filter(dateNtime__lte=datetime.now(), user=request.user).order_by('-dateNtime')[:1]
        home_page_vars = set_home_page_variables(user_posts, request.user)
        return JsonResponse(home_page_vars)

    return HttpResponse('')

def SaveMarker2(request):
    """" adds image/video to the object that was just made above """
    last_post_by_user = Post.objects.filter(user=request.user).last()
    last_post_by_user.attachment = request.FILES['attachment']
    last_post_by_user.save()

    # user is redirected to the profile after adding a post (marker)
    user_posts = Post.objects.filter(dateNtime__lte=datetime.now(), user=request.user).order_by('-dateNtime')[:1]
    home_page_vars = set_home_page_variables(user_posts, request.user)
    return JsonResponse(home_page_vars)
################################################################################


"""
once a marker is liked, an ajax is sent to this function. it receives the pk
or id of the marker which has just been liked. then it checks whether the user
has already liked this marker or not.

1.if it is already liked, the like by this user is removed from the database (it
is unliked)

2.if not already liked, a like object by this user for this marker is made (marker
is liked)

the function then sends back a JsonResponse, containing the current number of likes
for this marker (to be updated on the marker in front-end. so the user sees the
last number of likes). it also sends a flag: 0 means unliked, 1 means liked. this
is used for changing the color of like button: unliked is grey, liked is blue
"""
def likeMarker(request):
    post = Post.objects.get(pk=request.POST.get('pk'))
    liked = Like.objects.filter(user=request.user, post=post)
    if liked:
        liked.delete()
        flag = 0
    else:
        liked = Like(user=request.user, post=post)
        liked.save()
        flag = 1
    num_likes = Like.objects.filter(post=post).count()
    return JsonResponse({'num_likes': num_likes, 'flag': flag})


"""
this function is unfinished. it saves the comment added by the user to the database
"""
def commentMarker(request):
    body = request.POST.get('comment')
    post = Post.objects.get(pk=request.POST.get('id'))
    comment = Comment(user=request.user, post=post, body=body)
    comment.save()
    return JsonResponse({'c': body})


"""
deletes the markers once user clickes on (own's post) delete button. removes
the marker from the database and then redirects to the last marker by the user
"""
def deleteMarker(request):
    """deletes the marker from the database"""
    user = request.user
    date = request.POST.get('date')
    post = Post.objects.filter(dateNtime__gte=date, user=user).first()
    post.delete()

    user_posts = user.post_set.order_by('-dateNtime')[:1]
    user_posts = set_home_page_variables(user_posts, user)
    return JsonResponse(user_posts)


# no searching for posts at the moment!
"""def first_results(requests):
    SearchQueries.objects.all().delete()
    query = Post.objects.filter(title__contains=requests.POST.get('q'))
    for q in query:
        SearchQueries.objects.create( title=q.title,
                                      youtube_url=q.youtube_url,
                                      latitude=q.latitude,
                                      longitude=q.longitude )
    posts = SearchQueries.objects.filter(dateNtime__lte=datetime.now()).order_by('-dateNtime')[:2]

    home_page_vars = set_home_page_variables(posts)
    return JsonResponse(home_page_vars)
def next_results(requests):
    home_page_vars = {}
    date = literal_eval(requests.POST.get('date'))
    key  = requests.POST.get('key')
    number = int(requests.POST.get('number'))
    if number == 0: number = 1
    elif number > 5: number = 5

    if key == 'old':   # older markers
        if number != 1:
            posts = SearchQueries.objects.filter(dateNtime__lte=date).order_by('-dateNtime')[:number]
        else:
            posts = SearchQueries.objects.filter(dateNtime__lte=date).order_by('-dateNtime')[:2]
    else:   # newer markers
        if number != 1:
            posts = SearchQueries.objects.filter(dateNtime__gte=date).order_by('dateNtime')[:number]
        else:
            posts = SearchQueries.objects.filter(dateNtime__gte=date).order_by('dateNtime')[:2]

    if number == 1:
        home_page_vars = set_home_page_variables(posts,1)
    else:
        home_page_vars = set_home_page_variables(posts, number)
    return JsonResponse(home_page_vars)
    """
