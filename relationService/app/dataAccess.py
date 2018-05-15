"""
____________________________________________________
 Copyright 2018 Yicong Gong
 All rights reserved, for demostration purpose only.
____________________________________________________
This file provides application specific data-access functions.

"""
# table names
FRIEND_TABLE = 'relationService_Friend'
MOMENT_TABLE = 'relationService_Moment'

from datetime import datetime
import dynamoAccess

# follow a friend
def add_follow(from_ID, to_ID):
    time = str(datetime.now())
    response = dynamoAccess.add(FRIEND_TABLE, 'publisher', to_ID, 'subscriber', from_ID, time = time)
    return response

# unfollow a friend
def delete_follow(publisher, subscriber):
    time = str(datetime.now())
    response = dynamoAccess.delete(FRIEND_TABLE, 'publisher', publisher, 'subscriber', subscriber)
    return response

# user post a moment
def add_post(moment_ID, attraction_ID, user_ID):
    time = str(datetime.now())
    response = dynamoAccess.add(MOMENT_TABLE, 'user_ID', user_ID, 'moment_ID', moment_ID, attraction_ID = attraction_ID)
    return response

# get a list of followers
def get_followers(user_ID):
    response = dynamoAccess.query(FRIEND_TABLE, 'publisher', user_ID)
    friendList = []
    if response:
        for friend in response:
            friendList.append(friend['subscriber'])
    return friendList

# get a dict list of moments from a user
def get_moments(user_ID):
    response = dynamoAccess.query(MOMENT_TABLE, 'user_ID', user_ID)
    momentDictList = []
    if response:
        momentDictList = response
    return momentDictList
