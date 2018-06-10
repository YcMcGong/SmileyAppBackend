"""
____________________________________________________
 Copyright 2018 Yicong Gong
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
    old_attraction = get_attraction(attraction_ID)
    if old_attraction: 
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
        return status
    else:
        response = dynamoAccess.add(ATTRACTION_TABLE, 'attraction_ID', attraction_ID，'user_ID', user_ID, 'longitude', longitude, 'latitude', latitude, 'intro', intro, 'resource', resource, 'created_time', time, 'updated_time', time)
    return response

# create new moment under attraction or rewrite moment
def write_moment(MOMENT_TABLE, attraction_ID, moment_ID, user_ID, intro, resource):
    time = str(datetime.now())
    # check attraction existance to determin create new or update current
    old_moment = get_moment(moment_ID)
    if old_moment: 
        if user_ID:
            old_moment['user_ID'] = user_ID
        if intro:
            old_attraction['intro'] = intro
        if resource:
            old_attraction['resource'] = resource
        dynamoAccess.add(MOMENT_TABLE, 'attraction_ID', attraction_ID, 'moment_ID', moment_ID, 'user_ID', old_moment['user_ID'], 'intro', old_moment['intro'], 'resource', oldmoment['resource'], 'created_time', old_moment['created_time'], 'updated_time', time)
    else:
        dynamoAccess.add(MOMENT_TABLE, 'attraction_ID', attraction_ID, 'moment_ID', moment_ID, 'user_ID', user_ID, 'intro', intro, 'resource', resource, 'created_time', time, 'updated_time', time)
       
# get one attraction without resource
def get_attraction(attraction_ID):
    return dynamoAccess.get_item(ATTRACTION_TABLE, 'attraction_ID', attraction_ID)

# get one moment without resource
def get_moment(attraction_ID, moment_ID):
    return dynamoAccess.get_item(MOMENT_TABLE, 'attraction_ID', attraction_ID, 'moment_ID', moment_ID)

# admin access only
def delete_attraction(attraction_ID):
    dynamoAccess.delete(ATTRACTION_TABLE, 'attraction_ID', attraction_ID)

# delete one moment, only admin and the user can delete
def delete_moment(attraction_ID, moment_ID):
    dynamoAccess.delete(MOMENT_TABLE, 'attraction_ID', attraction_ID, 'moment_ID', moment_ID)
# unit test
if __name__ == '__main__':
    # print(user_sign_up('test@gmail.com', '123', 'mc', 'king', 'user_01', job = 'student'))
    # print(user_log(user_ID = '773e4629-1049-561b-b35b-d58b0aaf8710', dataType = 'work', salary = 1000, job = 'teacher'))
    # print(user_authenticate(username = 'user_01', password='123'))
    # print(lookup_email('test@gmail.com'))
