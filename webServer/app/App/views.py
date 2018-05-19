import json
import os
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.template import Context, Template

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
    return 'Welcome to my smile app'

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
    return status.get_response()

# Login function
def user_login(request):
    status = status_response()
    if request.method == 'POST':
        # Read data
        email = request.form.get('email')
        username = request.form.get('username')
        user_ID = request.form.get('user_ID')
        password = request.form.get('password')

        response = serviceAPI.authService.user_authenticate(email=email, username=username, user_ID=user_ID, password=password)

        if response['status']:
            # Associate the request with the user_id on local session DB
            user_id = response['user_ID']
            current_user.login_user(request, user_id)
            status.set_status(True)
    return status.get_response()

# Logout function
def user_logout(request):
    status = status_response()
    if request.method == 'GET':
        current_user.logout_user(request)
        status.set_status(True)
    return status.get_response()

# Create User
def create_user(request):
    status = status_response()
    if request.method == 'POST':
        # Read data
        email = request.form.get('email')
        password = request.form.get('password')
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        username = request.form.get('username')

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
    return status.get_response()           

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
    return status.get_response() 

# Get profile information
def get_profile(request):
    status = status_response()
    if request.method == 'GET':
        # Read data
        email = request.args.get('email')
        username = request.args.get('username')
        user_ID = request.args.get('user_ID')
        data = serviceAPI.authService.user_get_profile(user_ID=user_ID, username=username, email=email)

        if data['status']:
            status.attach_data('data', data, isSuccess=True)
    return status.get_response() 

"""
#  ________________________________________
# | Friend & Relationship Section          |
# |________________________________________|
"""
def get_friendlist(request):
    status = status_response()
    # Get friend list
    if request.method == 'GET':
        data = serviceAPI.relationService.list_all_friends(current_user.get_user_id(request))
        if data['status']:
            status.attach_data('data', data, isSuccess=True)
    
    # Follow a friend
    elif request.method == 'POST':
        follow_ID = request.form.get('follow_ID')
        response = serviceAPI.relationService.add_follow(follow_ID)
        if response['status']:
            status.attach_data('data', data, isSuccess=True)

    # Delete a friend
    elif request.method == 'DELETE':
        email = request.args.get('email')
        follow_ID = request.form.get('follow_ID')
        response = serviceAPI.relationService.delete_follow(follow_ID)
        if response['status']:
            status.attach_data('data', data, isSuccess=True)

    return status.get_response()
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
    return status.get_response()

"""
#  ________________________________________
# | Attraction related Session             |
# |________________________________________|
"""

# Attraction View
def new_moment(request):
    status = status_response()
    # Create an attraction
    if request.method == 'POST':
        # Read Data
        name = request.form.get('name')
        lat = request.form.get('lat')
        lng = request.form.get('lng')
        intro = request.form.get('intro')
        rating = request.form.get('rating')

        # Calculate the score based on the user experience and the rating
        score = (float(rating) + 10)

        user_ID = current_user.get_user_id(request)
        
        response = serviceAPI.attractionService.postMoment(name, lat, lng, intro, rating, user_ID)
        if response['status']:
            status.set_status(True)
    return status.get_response()
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
        lat = request.args.get('lat')
        lng = request.args.get('lng')
        data = serviceAPI.attractionService.findNearbyAttraction(lat, lng)
        if data['status']:
            status.set_status(True)
    return status.get_response()

"""
#  ________________________________________
# |All Web Relation Content below this line|
# |________________________________________|
"""

# No login required
def request_place_look_up(request):
    status = status_response()
    if request.method == 'GET':
        attraction_ID = request.args.get('attraction_ID')
        user_ID = current_user.get_user_id(request)
        data = serviceAPI.mapService.get_attraction_moment(user_ID, attraction_ID)
        if data['status']:
            status.attach_data('data', data, isSuccess=True)
    return status.get_response()
