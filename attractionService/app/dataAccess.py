"""
____________________________________________________
 Copyright 2018 Bangtian Zhou
 All rights reserved, for demostration purpose only.
____________________________________________________
This file provides application specific data-access functions.

"""
# table names
ATTRACTION_TABLE = 'attractionService_Attraction'
MOMENT_TABLE = 'relationService_Moment'

from time import gmtime, strftime
import dynamoAccess
import S3Access
import uuid
import hmac

# create new attraction or rewrite attraction
def write_attraction(attraction_ID, user_ID, longitude, latitude, intro, resource):
    status = status_response()
    time = str(datetime.now())
    # check attraction existance to determin create new or update current
    old_attraction_response = get_attraction(attraction_ID)
    if old_attraction_response.data['status']:
        old_attraction = old_attraction_response.data['attraction'] 
        if user_ID:
            if old_attraction['user_ID'] == user_ID or isAdmin(user_ID):
                if longitude:
                    old_attraction['longitude'] = longitude
                if latitude:
                    old_attraction['latitude'] = latitude
                if intro:
                    old_attraction['intro'] = intro
                if resource:
                    old_attraction['resource'] = resource
                response = dynamoAccess.add(ATTRACTION_TABLE, 'attraction_ID', attraction_ID，'user_ID', old_attraction['user_ID'], 'longitude', old_attraction['longitude'], 'latitude', old_attraction['latitude'], 'intro', old_attraction['intro'], 'resource', old_attraction['resource'], 'created_time', old_attraction['created_time'], 'updated_time', time)
                if response:
                    status.set_status(True)
                else:
                    status.set_status(False)
                    status.set_errorMessage('error write into database')
            else: 
                status.set_status(False)
                status.set_errorMessage('Permision denied')
        else:
            status.set_status(False)
            status.set_errorMessage('user_ID not found')
    else:
        response = dynamoAccess.add(ATTRACTION_TABLE, 'attraction_ID', attraction_ID，'user_ID', user_ID, 'longitude', longitude, 'latitude', latitude, 'intro', intro, 'resource', resource, 'created_time', time, 'updated_time', time)
        if response:
            status.set_status(True)
        else:
            status.set_status(False)
            status.set_errorMessage('error write into database')
    return status

# create new moment under attraction or rewrite moment
def write_moment(MOMENT_TABLE, attraction_ID, moment_ID, user_ID, intro, resource):
    time = str(datetime.now())
    status = status_response()
    # check attraction existance to determin create new or update current
    old_moment_response = get_moment(attraction_ID, moment_ID)
    if old_moment_response.data['status']:
        old_moment = old_moment_response.data['moment'] 
        if user_ID:
            if old_moment['user_ID'] == user_ID or isAdmin(user_ID):
                if intro:
                    old_moment['intro'] = intro
                if resource:
                    old_moment['resource'] = resource
                response = dynamoAccess.add(MOMENT_TABLE, 'attraction_ID', attraction_ID, 'moment_ID', moment_ID, 'user_ID', old_moment['user_ID'], 'intro', old_moment['intro'], 'resource', oldmoment['resource'], 'created_time', old_moment['created_time'], 'updated_time', time)
                if response:
                    status.set_status(True)
                else:
                    status.set_status(False)
                    status.set_errorMessage('error write into database')
            else: 
                status.set_status(False)
                status.set_errorMessage('Permision denied')
        else:
            status.set_status(False)
            status.set_errorMessage('user_ID not found')
    else:
        response = dynamoAccess.add(MOMENT_TABLE, 'attraction_ID', attraction_ID, 'moment_ID', moment_ID, 'user_ID', user_ID, 'intro', intro, 'resource', resource, 'created_time', time, 'updated_time', time)
        if response:
            status.set_status(True)
        else:
            status.set_status(False)
            status.set_errorMessage('error write into database')
    return status   

# get one attraction without resource
def get_attraction(attraction_ID):
    response = dynamoAccess.get_item(ATTRACTION_TABLE, 'attraction_ID', attraction_ID)
    status = status_response()
    if response:
        status.attach_data('attraction', response, True)
    else:
        status.set_status(False)
        status.set_errorMessage('error get attraction from database')
    return status

# get one moment without resource
def get_moment(attraction_ID, moment_ID):
    response = dynamoAccess.get_item(MOMENT_TABLE, 'attraction_ID', attraction_ID, 'moment_ID', moment_ID)
    status = status_response()
    if response:
        status.attach_data('moment', response, True)
    else:
        status.set_status(False)
        status.set_errorMessage('error get moment from database')
    return status

# admin access only
def delete_attraction(attraction_ID, user_ID):
    status = status_response()
    if isAdmin(user_ID):
        response = dynamoAccess.delete(ATTRACTION_TABLE, 'attraction_ID', attraction_ID)
        if response:
            status.set_status(True)
        else:
            status.set_status(False)
            status.set_errorMessage('error delete attraction from database')
    else:
        status.set_status(False)
        status.set_errorMessage('permission denied')
    return status

# delete one moment, only admin and the user can delete
def delete_moment(attraction_ID, moment_ID, user_ID):
    status = status_response()
    old_moment_response = get_moment(attraction_ID, moment_ID)
    if old_moment_response.data['status']:
        old_moment = old_moment_response.data['moment']
        if user_ID:
            if old_moment['user_ID'] == user_ID or isAdmin(user_ID):
                response = dynamoAccess.delete(MOMENT_TABLE, 'attraction_ID', attraction_ID, 'moment_ID', moment_ID)
                if response:
                    status.set_status(True)
                else:
                    status.set_status(False)
                    status.set_errorMessage('error delete moment database')
            else: 
                status.set_status(False)
                status.set_errorMessage('Permision denied')
        else:
            status.set_status(False)
            status.set_errorMessage('user_ID not found')
    else:
        status.set_status(False)
        status.set_errorMessage('moment not found')
    return status

# unit test
if __name__ == '__main__':
    # print(user_sign_up('test@gmail.com', '123', 'mc', 'king', 'user_01', job = 'student'))
    # print(user_log(user_ID = '773e4629-1049-561b-b35b-d58b0aaf8710', dataType = 'work', salary = 1000, job = 'teacher'))
    # print(user_authenticate(username = 'user_01', password='123'))
    # print(lookup_email('test@gmail.com'))
