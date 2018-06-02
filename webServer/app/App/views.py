import json
import os
from django.http import JsonResponse, QueryDict, HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import Context, Template
from django.views.decorators.csrf import csrf_exempt

# import utility
from utility import current_user
from utility.utilities import status_response
import serviceAPI

"""
#  ________________________________________
# |Health Check                            |
# |________________________________________|
"""
def welcome(request):
    HttpResponse('Welcome to my smile app')

"""
#  ________________________________________
# |User & Login Related Sessions           |
# |________________________________________|
"""
# PreLogin check if session expired
def pre_user_login(request):
    status = status_response()
    if request.method == 'GET':
        if request.user.is_authenticated:
            status.set_status(True)
    return JsonResponse(status.data)

# Login function
@csrf_exempt
def user_login(request):
    status = status_response()
    if request.method == 'POST':
        # Read data
        email = request.POST.get('email')
        username = request.POST.get('username')
        user_ID = request.POST.get('user_ID')
        password = request.POST.get('password')

        response = serviceAPI.authService.user_authenticate(email=email, username=username, user_ID=user_ID, password=password)

        if response['status']:
            # Associate the request with the user_id on local session DB
            user_id = response['user_ID']
            current_user.login_user(request, user_id)
            status.set_status(True)
    return JsonResponse(status.data)

# Logout function
def user_logout(request):
    status = status_response()
    if request.method == 'GET':
        current_user.logout_user(request)
        status.set_status(True)
    return JsonResponse(status.data)

# Create User
@csrf_exempt
def create_user(request):
    status = status_response()
    if request.method == 'POST':
        # Read data
        email = request.POST.get('email')
        password = request.POST.get('password')
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        username = request.POST.get('username')

        # Check if all fields valid
        if email and password and firstName and lastName and username:
            response = serviceAPI.authService.user_create(email, firstName, lastName, username ,password)
            if response['status']:
                # Automatically log in the use after sign up
                user_ID = response['user_ID']
                current_user.login_user(request, user_ID)
                status.set_status(True)
            else:
                status.set_errorMessage('DB failed')
        else:
            status.set_errorMessage('fields not valid')
    return JsonResponse(status.data)           

"""
#  ________________________________________
# | Profile Session                        |
# |________________________________________|
"""
# Get profile information
def get_my_profile(request):
    status = status_response()
    if request.method == 'GET':
        # Read data
        user_ID = current_user.get_user_id(request)
        data = serviceAPI.authService.user_get_profile(user_ID=user_ID)

        if data['status']:
            status.attach_data('data', data, isSuccess=True)
    return JsonResponse(status.data) 

# Get profile information
def get_profile(request):
    status = status_response()
    if request.method == 'GET':
        # Read data
        email = request.GET.get('email')
        username = request.GET.get('username')
        user_ID = request.GET.get('user_ID')
        data = serviceAPI.authService.user_get_profile(user_ID=user_ID, username=username, email=email)

        if data['status']:
            status.attach_data('data', data, isSuccess=True)
    return JsonResponse(status.data) 

"""
#  ________________________________________
# | Friend & Relationship Section          |
# |________________________________________|
"""
@csrf_exempt
def get_friendlist(request):
    status = status_response()
    # Get friend list
    if request.method == 'GET':
        data = serviceAPI.relationService.list_all_friends(current_user.get_user_id(request))
        if data['status']:
            status.attach_data('data', data, isSuccess=True)
    
    # Follow a friend
    elif request.method == 'POST':
        follow_ID = request.POST.get('follow_ID')
        response = serviceAPI.relationService.add_follow(follow_ID)
        if response['status']:
            status.attach_data('data', data, isSuccess=True)

    # Delete a friend
    elif request.method == 'DELETE':
        email = QueryDict(request.body).get('email')
        follow_ID = QueryDict(request.body).get('follow_ID')
        response = serviceAPI.relationService.delete_follow(follow_ID)
        if response['status']:
            status.attach_data('data', data, isSuccess=True)

    return JsonResponse(status.data)
"""
#  ________________________________________
# | Map related Session                    |
# |________________________________________|
"""
# Map view
def get_map(request):
    status = status_response()
    if request.method == 'GET':
        data = serviceAPI.mapService.load_map(current_user.get_user_id(request))
        if data['status']:
            status.attach_data('data', data, isSuccess=True)
    return JsonResponse(status.data)

"""
#  ________________________________________
# | Attraction related Session             |
# |________________________________________|
"""

# Attraction View
@csrf_exempt
def new_moment(request):
    status = status_response()
    # Create an attraction
    if request.method == 'POST':
        # Read Data
        name = request.POST.get('name')
        lat = request.POST.get('lat')
        lng = request.POST.get('lng')
        intro = request.POST.get('intro')
        rating = request.POST.get('rating')

        # Calculate the score based on the user experience and the rating
        score = (float(rating) + 10)

        user_ID = current_user.get_user_id(request)
        
        response = serviceAPI.attractionService.postMoment(name, lat, lng, intro, rating, user_ID)
        if response['status']:
            status.set_status(True)
    return JsonResponse(status.data)
# return marker

"""
#  ________________________________________
# | Location Service section               |
# |________________________________________|
"""
# Return the places nearby to the front end for selection
def get_list_of_places_near_a_coordinate(request):
    status = status_response()
    if request.method == 'GET':
        lat = request.GET.get('lat')
        lng = request.GETs.get('lng')
        data = serviceAPI.attractionService.findNearbyAttraction(lat, lng)
        if data['status']:
            status.set_status(True)
    return JsonResponse(status.data)

"""
#  ________________________________________
# |All Web Relation Content below this line|
# |________________________________________|
"""

# No login required
def request_place_look_up(request):
    status = status_response()
    if request.method == 'GET':
        attraction_ID = request.GET.get('attraction_ID')
        user_ID = current_user.get_user_id(request)
        data = serviceAPI.mapService.get_attraction_moment(user_ID, attraction_ID)
        if data['status']:
            status.attach_data('data', data, isSuccess=True)
    return JsonResponse(status.data)
