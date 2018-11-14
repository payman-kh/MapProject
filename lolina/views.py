from django.shortcuts import render , redirect
from django.http import JsonResponse, HttpResponse
from .models import Post #, SearchQueries
#from users.models import Profile
from django.contrib.auth.models import User
import json
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime
import requests
from ast import literal_eval
from urllib.parse import unquote
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import os


def set_home_page_variables(posts, number=1, ):
    home_page_dict = {}
    if posts:
        json_serializer = serializers.get_serializer("json")()
        markers_json = json_serializer.serialize(posts  , ensure_ascii=False)

        user_names  = [ u.user.username for u in posts ]
        image_urls  = [ i.user.profile.image.url for i in posts ]
        user_names_json =  json.dumps(user_names, cls=DjangoJSONEncoder)
        image_urls_json =  json.dumps(image_urls, cls=DjangoJSONEncoder)

        posts_list = posts.values()
        datetimes  = [ d['dateNtime'] for d in posts_list ]
        min_datetime = str(min(datetimes))
        max_datetime = str(max(datetimes))
        min_datetime_json =  json.dumps(min_datetime, cls=DjangoJSONEncoder)
        max_datetime_json =  json.dumps(max_datetime, cls=DjangoJSONEncoder)

        home_page_dict = {'markers_json': markers_json,
                          'user_names'  : user_names_json,
                          'image_urls'  : image_urls_json,
                          'min_datetime': min_datetime_json,
                          'max_datetime': max_datetime_json,
                          'number'      : number}
    return home_page_dict


def get_latest_markers(requests):
    user = requests.user
    posts = Post.objects.exclude(user=user).filter(dateNtime__lte=datetime.now()).order_by('-dateNtime')[:1]
    #posts = Post.objects.exclude(user=user).order_by('-dateNtime')[:1]
    home_page_vars = set_home_page_variables(posts)
    return JsonResponse(home_page_vars)


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
            home_page_vars = set_home_page_variables(posts, number)
            return JsonResponse(home_page_vars)

        else:       # first time homepage load
            posts = Post.objects.exclude(user=user).order_by('-dateNtime')[:2]
            home_page_vars = set_home_page_variables(posts, 1)
            return render(requests, 'map.html', home_page_vars)
    else:
        return redirect('login')


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


#TODO merge these two views. there's gotta be better ways doing this
# this way of savig forms with double functions/ajaxes is really wird
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
        home_page_vars = set_home_page_variables(user_posts)
        return JsonResponse(home_page_vars)

    return HttpResponse('')

def SaveMarker2(request):
    """" adds image/video to the object that was just made above """
    #TODO: it is unstable and error prone to simply get the last one. we need a
    # way to look for the associated object more precisely
    last_post_by_user = Post.objects.filter(user=request.user).last()
    last_post_by_user.attachment = request.FILES['attachment']
    last_post_by_user.save()

    # user is redirected to the profile after adding a post (marker)
    user_posts = Post.objects.filter(dateNtime__lte=datetime.now(), user=request.user).order_by('-dateNtime')[:1]
    home_page_vars = set_home_page_variables(user_posts)
    return JsonResponse(home_page_vars)
################################################################################


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
