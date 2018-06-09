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

def write_attraction(attraction_ID, user_ID, longitude, latitude, intro, resource):
    dynamoAccess.add(ATTRACTION_TABLE, 'attraction_ID', attraction_ID，'user_ID', user_ID, 'longitude', longitude, 'latitude', latitude, 'intro', intro, resource)

def write_moment(MOMENT_TABLE, attraction_ID, moment_ID, user_ID, intro, resource):
    dynamoAccess.add(MOMENT_TABLE, 'attraction_ID', attraction_ID, 'moment_ID', moment_ID, 'user_ID', user_ID, 'intro', intro, 'resource', resource)

# unit test
if __name__ == '__main__':
    # print(user_sign_up('test@gmail.com', '123', 'mc', 'king', 'user_01', job = 'student'))
    # print(user_log(user_ID = '773e4629-1049-561b-b35b-d58b0aaf8710', dataType = 'work', salary = 1000, job = 'teacher'))
    # print(user_authenticate(username = 'user_01', password='123'))
    # print(lookup_email('test@gmail.com'))
