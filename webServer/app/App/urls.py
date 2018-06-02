from django.urls import path
from . import views

urlpatterns = [
    # Health Check

    # User & Login
    path('', views.welcome, name='welcome'),
    path('/pre_user_login', views.pre_user_login, name='pre_user_login'),
    path('/user_login', views.user_login, name='user_login'),
    path('/user_logout', views.user_logout, name='user_logout'),
    path('/create_user', views.create_user, name='create_user'),

    # get profile
    path('/my_profile', views.get_my_profile, name='get_my_profile'),
    path('/profile', views.get_profile, name='get_profile'),

    # Friendlist
    path('/friendlist', views.get_friendlist, name='friendlist'),

    # Map
    path('/map', views.get_map, name='get_map'),

    # Attraction
    path('/attraction', views.new_moment, name='new_moment'),
    path('/get_list_of_places_near_a_coordinate', views.get_list_of_places_near_a_coordinate, name='get_list_of_places_near_a_coordinate'),

    # Place
    path('/LookUpPlace', views.request_place_look_up, name='request_place_look_up')
]