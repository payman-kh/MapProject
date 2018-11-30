from django.conf.urls import url
from django.urls import path #, include
from django.contrib import admin
from lolina import views
from users import views as user_views
from django.contrib.auth import views as auth_views


urlpatterns = [
    # admin page
    url(r'^admin/', admin.site.urls),

    # sign-up page
    path('', user_views.signup, name='signup'),
    # login and logout
    path('login/', auth_views.LoginView.as_view(template_name='login.html',
                                                redirect_authenticated_user=True),
                                                name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    # delete Account
    path('deleteAccount/', user_views.deleteAccount, name="DeleteAccount"),

    #  home"page":
    url(r'^homepage/', views.homepage, name='homepage'),

    # profile "page"
    path('users/profile/', user_views.profile, name='profile'),
    # profile edit window
    path('users/profile_edit_window/', user_views.profile_edit_window, name='profile_edit_window'),
    # update profile info
    path('users/update_profile_info/', user_views.update_profile_info, name='update_profile_info'),
    # update profile image
    path('users/update_profile_image/', user_views.update_profile_image, name='update_profile_image'),
    # navigate through profile posts
    path('users/navigate_profile/', user_views.navigate_profile, name='navigate_profile'),
    # another users's profile picture
    path('users/user_profile_picture/', user_views.get_user_profile_picture, name='user_profile_picture'),

    # search function: (users)
    path('search/', views.Search, name='Search'),
    #url(r'^first_results/$', views.first_results, name='first_results'),
    #url(r'^next_results/$', views.next_results, name='next_results'),

    # save a new marker
    path('saveMarker1/', views.SaveMarker1, name='SaveMarker1'),
    path('saveMarker2/', views.SaveMarker2, name='SaveMarker2'),
    # like a marker
    path('likeMarker/', views.likeMarker, name='LikeMarker'),
    # comment a marker
    path('commentMarker/', views.commentMarker, name='CommentMarker'),
    # delete a marker
    path('deleteMarker/', views.deleteMarker, name='DeleteMarker'),

    # getting the latest marker after map loads:
    url(r'^get_latest_markers/$', views.get_latest_markers, name='get_latest_markers'),

    # showing the event marker (as example):
    #url(r'^event_marker/$', views.event_marker, name='event_marker'),

    # TODO (maybe): saving the marker with class-based views
    #url(r'^saveMarker/$', views.SaveMarkerView.as_view(), name='saveMarker')
]


from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
